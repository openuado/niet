#!/usr/bin/python
import argparse
import json
import sys
import textwrap

import pkg_resources
import pytoml as toml
import yaml
from jmespath import search
from jmespath.exceptions import LexerError

import niet.output as output
import niet.url

VALID_PRINTERS = {
    "json": {
        "cmd": output.print_json,
        "epilog": "Return object in JSON",
    },
    "yaml": {
        "cmd": output.print_yaml,
        "epilog": "Return object in YAML",
    },
    "toml": {
        "cmd": output.print_toml,
        "epilog": "Return object in TOML",
    },
    "eval": {
        "cmd": output.print_eval,
        "epilog": "Return result in a string evaluable by a shell "
        "eval command as an input",
    },
    "newline": {
        "cmd": output.print_newline,
        "epilog": "Return all elements of a list in a new line",
    },
    "ifs": {
        "cmd": output.print_ifs,
        "epilog": "Return all elements of a list separated by IFS env var",
    },
    "squote": {
        "cmd": output.print_squote,
        "epilog": "Add single quotes to result",
    },
    "dquote": {
        "cmd": output.print_dquote,
        "epilog": "Add double quotes to result",
    },
    "comma": {
        "cmd": output.print_comma,
        "epilog": "Return all elements separated by commas",
    },
}


def get_epilog():
    epilog = ""
    indent_max = max(VALID_PRINTERS.keys(), key=len)
    for item in VALID_PRINTERS:
        epilog += "  {item}{indent}\t{epilog}\n".format(
            item=item,
            indent=" " * (len(indent_max) - len(item)),
            epilog=VALID_PRINTERS[item]["epilog"],
        )
    return epilog


class ContentType(argparse.FileType):
    def __call__(self, string):
        if niet.url.is_webresource(string):
            return string
        return super().__call__(string)


# arguments parsing
def argparser():
    epilog = """output formats:\n{}""".format(get_epilog())

    parser = argparse.ArgumentParser(
        description="Read data from YAML or JSON file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser.add_argument(
        "object",
        type=str,
        help="Path to object separated by dot (.). \
                        Use '.' to get whole file. \
                        eg: a.b.c",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=ContentType(),
        help="Optional JSON or YAML local filename or \
                        distant web resource at raw format. \
                        If not provided niet read from stdin",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=[key for key in VALID_PRINTERS],
        help="output format",
    )
    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Perform modification in place. Will so alter \
                        read file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="OUTPUT_FILE",
        help="Print output in a file instead of stdout \
                        (surcharged by in-place parameter if set)",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="silent mode, doesn't display message when \
                        element was not found",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the Niet version number and \
                        exit (also --version)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Activate the debug mode (based on pdb)"
    )
    return parser.parse_args()


# Parsing to extract wanted object
def data_parser(dataset):
    result = None
    try:
        result = json.loads(dataset)
        in_format = "json"
    except ValueError:
        try:
            result = yaml.safe_load(dataset)
            in_format = "yaml"
        except (yaml.constructor.ConstructorError, yaml.parser.ParserError) as err:
            try:
                result = toml.loads(dataset)
                in_format = "toml"
            except toml.core.TomlError as err:
                print(str(err))
    if not isinstance(result, (list, dict)):
        print(
            textwrap.dedent(
                """
                Oops... An error occur.
                You face this error because the passed file has been
                detected as invalid. It have been detected invalid because
                either the format of this file isn't correct or
                unsupported.

                Niet only support valid json, yaml, and toml input.
                You can check that your file is valid by using a JSON or
                YAML linter. https://jsonlint.com/"""
            )
        )
        sys.exit(1)
    return result, in_format


# Load file
def get(data, keywords, silent=False):
    if keywords == ".":
        return data
    if keywords.startswith("."):
        keywords = keywords[1:]
    cursor = None
    try:
        try:
            cursor = search(keywords, data)
        except LexerError:
            cursor = search('"{keywords}"'.format(keywords=keywords), data)
        if not cursor and cursor != False and cursor != 0:
            raise KeyError()
        return cursor
    except (KeyError, AttributeError):
        if not silent:
            print("Element not found: {research}".format(research=keywords))
        sys.exit(1)


def print_result(res, out_format, in_format, search, out_file):
    if out_format is None:
        if isinstance(res, (list, str, int, float)) or in_format is None:
            out_format = "newline"
        else:
            out_format = in_format
    try:
        if out_format == "eval":
            output = VALID_PRINTERS[out_format]["cmd"](res, search)
        else:
            # we need to pass the search to init the eval var name
            output = VALID_PRINTERS[out_format]["cmd"](res)
    except KeyError:
        print(f"Error : Invalid choice ({out_format}). ")
        print("Supported formats are: {format}".format(",".join(VALID_PRINTERS)))
    else:
        if out_file:
            with open(out_file, "w+") as f:
                f.write(output)
        else:
            print(output)


def get_data(infile):
    # NOTE(hberaud): if infile is a string then we deal with a web resource
    if isinstance(infile, str):
        return infile
    with infile:
        return infile.read()


def version():
    installed = pkg_resources.get_distribution("niet").version
    print("niet version {}".format(installed))


# Main
def main():
    if "-v" in sys.argv or "--version" in sys.argv:
        version()
        sys.exit(0)
    args = argparser()
    if args.debug:
        import pdb

        pdb.set_trace()
    infile = args.file or sys.stdin
    if isinstance(infile, str):
        # NOTE(hberaud): We consider we using a web resource if
        # infile is a string
        infile = niet.url.fetch(infile)
    else:
        # NOTE(hberaud): web resources can't be modified in place so we
        # don't need to do this
        infilename = args.file.name if args.file else ""
    search = args.object
    dataset = get_data(infile)
    # NOTE(hberaud): if infile is a string then we deal with a web resource
    # else (not a string) infile is a file pointer who must be closed
    if not isinstance(infile, str):
        infile.close()
    out_format = args.format
    out_file = args.output
    silent = args.silent
    data, in_format = data_parser(dataset)
    result = get(data, search, silent)

    if args.in_place and infilename:
        out_file = infilename

    print_result(result, out_format, in_format, search, out_file)

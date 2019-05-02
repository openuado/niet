#!/usr/bin/python
import argparse
import json
import os.path
import sys

from future.utils import viewitems

from jmespath import search

import pkg_resources

import yaml


IFS = os.getenv('IFS', ' ')


# Output functions
def out_print_squote(res):
    if isinstance(res, list):
        res = IFS.join(["'{}'".format(el) for el in res])
    elif (isinstance(res, str) or isinstance(res, int)):
        res = "".join("'{}'".format(res))
    return res


def out_print_dquote(res):
    if isinstance(res, list):
        res = IFS.join(["\"{}\"".format(el) for el in res])
    elif (isinstance(res, str) or isinstance(res, int)):
        res = "".join("\"{}\"".format(res))
    return res


def out_print_ifs(res):
    if isinstance(res, list):
        res = IFS.join(["{}".format(el) for el in res])
    return res


def out_print_newline(res):
    if isinstance(res, list):
        try:
            return '\n'.join(res)
        except TypeError:
            result = []
            for el in res:
                result.append(yaml.dump(el))
            return "".join(result)
    else:
        return res


def out_print_yaml(res):
    return yaml.dump(res, default_flow_style=False)


def out_print_json(res):
    return json.dumps(res, indent=4)


VALID_PRINTERS = {
    "json": {
        "cmd": out_print_json,
        "epilog": "Return object in JSON",
    },
    "yaml": {
        "cmd": out_print_yaml,
        "epilog": "Return object in YAML",
    },
    "newline": {
        "cmd": out_print_newline,
        "epilog": "Return all element of a list in a new line",
    },
    "ifs": {
        "cmd": out_print_ifs,
        "epilog": "Return all elements of a list separated by IFS env var",
    },
    "squote": {
        "cmd": out_print_squote,
        "epilog": "Add single quotes to result",
    },
    "dquote": {
        "cmd": out_print_dquote,
        "epilog": "Add double quotes to result",
    },
}


def get_epilog():
    epilog = ""
    for key, value in viewitems(VALID_PRINTERS):
        epilog += "  {}\t{}\n".format(key, value['epilog'])
    return epilog


# arguments parsing
def argparser():
    epilog = '''output formats:\n{}'''.format(get_epilog())

    parser = argparse.ArgumentParser(
        description='Read data from YAML or JSON file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog)
    parser.add_argument('object', type=str,
                        help="Path to object separated by dot (.). \
                        Use '.' to get whole file. \
                        eg: a.b.c")
    parser.add_argument('file', nargs='?', type=argparse.FileType(),
                        help="Optional JSON or YAML filename. \
                        If not provided niet read from stdin")
    parser.add_argument('-f', '--format', type=str,
                        choices=[key for key in VALID_PRINTERS],
                        help="output format")
    parser.add_argument('-s', '--silent', action='store_true',
                        help="silent mode, doesn't display message when \
                        element was not found")
    parser.add_argument('-v', '--version', action='store_true',
                        help="print the Niet version number and \
                        exit (also --version)")
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
        except yaml.constructor.ConstructorError as err:
            print(str(err))
        except yaml.parser.ParserError as err:
            print(str(err))
    if not isinstance(result, (list, dict)):
        print("Invalid file. Only support valid json and yaml input")
        sys.exit(1)
    return result, in_format


# Load file
def get(data, keywords, silent=False):
    if keywords == ".":
        return data
    if keywords.startswith("."):
        keywords = keywords[1:]
    try:
        cursor = search(keywords, data)
        if not cursor:
            raise KeyError()
        return cursor
    except (KeyError, AttributeError):
        if not silent:
            print("Element not found: {research}".format(research=keywords))
        sys.exit(1)


def print_result(res, out_format, in_format):
    if out_format is None:
        if (isinstance(res, (list, str, int)) or in_format is None):
            out_format = "newline"
        else:
            out_format = in_format
    try:
        output = VALID_PRINTERS[out_format]["cmd"](res)
    except KeyError:
        print("Error : Invalid choice")
    else:
        print(output)


def get_data(infile):
    with infile:
        return infile.read()


def version():
    installed = pkg_resources.get_distribution('niet').version
    print("niet version {}".format(installed))


# Main
def main():
    if '-v' in sys.argv or '--version' in sys.argv:
        version()
        sys.exit(0)
    args = argparser()
    infile = args.file or sys.stdin
    search = args.object
    dataset = get_data(infile)
    out_format = args.format
    silent = args.silent
    data, in_format = data_parser(dataset)
    result = get(data, search, silent)
    print_result(result, out_format, in_format)

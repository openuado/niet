#!/usr/bin/python
import argparse
import json
import os.path
import sys
from future.utils import viewitems
import yaml


IFS = os.getenv('IFS', ' ')


# Output functions
def out_print_squote(res):
    if isinstance(res, list):
        res = IFS.join(["'{}'".format(el) for el in res])
    elif (isinstance(res, str) or isinstance(res, int)):
        res = "".join("'{}'".format(res))
    print(res)


def out_print_dquote(res):
    if isinstance(res, list):
        res = IFS.join(["\"{}\"".format(el) for el in res])
    elif (isinstance(res, str) or isinstance(res, int)):
        res = "".join("\"{}\"".format(res))
    print(res)


def out_print_ifs(res):
    if isinstance(res, list):
        res = IFS.join(["{}".format(el) for el in res])
    print(res)


def out_print_newline(res):
    if isinstance(res, list):
        print('\n'.join(res))
    else:
        print(res)


def out_print_yaml(res):
    print(yaml.dump(res, default_flow_style=False))


def out_print_json(res):
    print(json.dumps(res, indent=4))


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
    parser.add_argument('file', type=str,
                        help="JSON or YAML filename")
    parser.add_argument('object', type=str,
                        help="Path to object separated by dot (.). \
                        Use '.' to get whole file. \
                        eg: a.b.c")
    parser.add_argument('-f', '--format', type=str,
                        choices=[key for key in VALID_PRINTERS],
                        help="output format")
    args = parser.parse_args()
    return args.file, args.object, args.format


# Parsing to extract wanted object
def data_parser(filename):
    data = None
    with open(filename, 'r') as stream:
        content = "".join(stream.readlines())
        try:
            data = json.loads(content)
            in_format = "json"
        except ValueError:
            try:
                data = yaml.load(content)
                in_format = "yaml"
            except yaml.parser.ParserError as err:
                print(str(err))
    if not isinstance(data, dict):
        print("Invalid file. Only support valid json and yaml files")
        sys.exit(1)
    return data, in_format


# Load file
def get(data, keywords):
    try:
        cursor = data
        for keyword in keywords:
            if not '' == keyword:
                cursor = cursor.get(keyword)
        if not cursor:
            raise KeyError()
        return cursor
    except (KeyError, AttributeError):
        print("Element not found: {research}".format(
            research=".".join(keywords))
        )
        sys.exit(1)


def print_result(res, out_format, in_format):
    if out_format is None:
        if (isinstance(res, list) or isinstance(res, str) or
                isinstance(res, int) or
                in_format is None):
            out_format = "newline"
        else:
            out_format = in_format
    try:
        VALID_PRINTERS[out_format]["cmd"](res)
    except KeyError:
        print("Error : Invalid choice")


# Main
def main():
    filename, search, out_format = argparser()
    if not os.path.isfile(filename):
        print("Error: File {} not found!".format(filename))
        sys.exit(127)
    data, in_format = data_parser(filename)
    keywords = search.split(".")
    result = get(data, keywords)
    print_result(result, out_format, in_format)


if __name__ == "__main__":
    main()

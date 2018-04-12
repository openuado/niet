#!/usr/bin/python
import argparse
import json
import sys
import os.path
import yaml


# arguments parsing
def argparser():
    epilog = '''output formats:
  spaces    Return all elements of a list separated by spaces
  quotes    Add quotes to result
  newline   Return all element of a list in a new line
  yaml      Return object in YAML
  json      Return object in JSON
'''
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
                        choices=['spaces', 'quotes',
                                 'json', 'yaml', 'newline'],
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
        if '.' == keywords:
            return cursor
        for keyword in keywords:
            cursor = cursor.get(keyword)
        if not cursor:
            raise KeyError()
        return cursor
    except (KeyError, AttributeError):
        print("Element not found: {research}".format(
            research=".".join(keywords))
        )
        sys.exit(1)


# Output functions
def out_print_quotes(res):
    if isinstance(res, list):
        res = " ".join(["'{}'".format(el) for el in res])
    print(res)


def out_print_spaces(res):
    if isinstance(res, list):
        res = " ".join(["{}".format(el) for el in res])
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


def print_result(res, out_format, in_format):
    # for compatibility with python 2 and 3
    try:
        basestring
    except NameError:
        basestring = str

    if out_format is None:
        if (isinstance(res, list) or isinstance(res, basestring) or
                isinstance(res, int) or in_format is None):
            out_format = "newline"
        else:
            out_format = in_format
    eval("out_print_{}(res)".format(out_format))


# Main
def main():
    filename, search, out_format = argparser()
    if not os.path.isfile(filename):
        print("Error: File {} not found!".format(filename))
        print("Abort!")
        sys.exit(127)
    data, in_format = data_parser(filename)
    if not search == '.':
        keywords = search.split(".")
    else:
        keywords = search
    result = get(data, keywords)
    print_result(result, out_format, in_format)


if __name__ == "__main__":
    main()

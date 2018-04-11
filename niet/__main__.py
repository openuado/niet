#!/usr/bin/python
import argparse
import json
import sys
import os.path
import yaml


def argparser():
    epilog = '''output formats:
             quotes    Add quotes to result
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
                        choices=['quotes'],
                        help="output format")
    args = parser.parse_args()
    return args.file, args.object, args.format


def data_parser(filename):
    data = None
    with open(filename, 'r') as stream:
        content = "".join(stream.readlines())
        try:
            data = yaml.load(content)
        except yaml.parser.ParserError:
            try:
                data = json.loads(content)
            except ValueError as err:
                print(str(err))
    if not isinstance(data, dict):
        print("Invalid file. Only support valid json and yaml files")
        sys.exit(1)
    return data


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


def print_result(res, out_format):
    if isinstance(res, list):
        if 'quotes' == out_format:
            res = " ".join(["'{}'".format(el) for el in res])
        else:
            res = " ".join(["{}".format(el) for el in res])
    print(res)


def main():
    filename, search, out_format = argparser()
    if not os.path.isfile(filename):
        print("Error: File {} not found!".format(filename))
        print("Abort!")
        sys.exit(127)
    data = data_parser(filename)
    if not search == '.':
        keywords = search.split(".")
    else:
        keywords = search
    result = get(data, keywords)
    print_result(result, out_format)


if __name__ == "__main__":
    main()

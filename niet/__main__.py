#!/usr/bin/python
import argparse
import json
import sys
import os.path
import yaml


def argparser():
    parser = argparse.ArgumentParser(
        description='Read data from yaml or json file')
    parser.add_argument('file', type=str)
    parser.add_argument('object', type=str)
    args = parser.parse_args()
    return args.file, args.object


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
        for keyword in keywords:
            cursor = cursor.get(keyword)
            if isinstance(cursor, list):
                cursor = " ".join(["{}".format(el) for el in cursor])
        return cursor
    except (KeyError, AttributeError):
        print("Element not found: {research}".format(
            research=".".join(keywords))
        )
        sys.exit(1)


def main():
    filename, search = argparser()
    if not os.path.isfile(filename):
        print("Yaml file not found!")
        print("Abort!")
        sys.exit(1)
    data = data_parser(filename)
    keywords = search.split(".")
    print(get(data, keywords))


if __name__ == "__main__":
    main()

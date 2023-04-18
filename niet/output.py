import json
import os

import pytoml as toml
import yaml

IFS = os.getenv("IFS", " ")


# Output functions
def print_squote(res):
    if isinstance(res, list):
        res = IFS.join(["'{}'".format(el) for el in res])
    elif isinstance(res, str) or isinstance(res, int):
        res = "".join("'{}'".format(res))
    return res


def print_dquote(res):
    if isinstance(res, list):
        res = IFS.join(['"{}"'.format(el) for el in res])
    elif isinstance(res, str) or isinstance(res, int):
        res = "".join('"{}"'.format(res))
    return res


def print_ifs(res):
    if isinstance(res, list):
        res = IFS.join(["{}".format(el) for el in res])
    return res


def _formate_result_with_delimiter(res, delimiter):
    if isinstance(res, list):
        try:
            return delimiter.join(map(str, res))
        except TypeError:
            result = []
            for el in res:
                result.append(yaml.dump(el))
            return "".join(result)
    else:
        return res


def print_newline(res):
    return _formate_result_with_delimiter(res, delimiter="\n")


def print_comma(res):
    return _formate_result_with_delimiter(res, delimiter=",")


def _findevalitem(obj, base=""):
    if base.startswith("_"):
        base = base[1:]
    el = []
    for k, v in obj.items():
        k = k.replace("-", "_")
        k = k.replace('"', "_")
        if base and base != "":
            k = base + "__" + k
        if isinstance(v, dict):
            item = _findevalitem(v, k)
            if item is not None:
                el.extend(item)
            continue
        if isinstance(v, list):
            el.append("{k}=( {value} )".format(k=k, value=" ".join(v)))
            continue
        el.append('{k}="{v}"'.format(k=k, v=v))
    return el


def print_eval(res, search):
    search = search.replace(".", "_")
    search = search.replace("-", "_")
    search = search.replace('"', "")
    if type(res) == dict:
        results = _findevalitem(res, search)
        return ";".join(results)
    elif type(res) == list:
        return "{key}=( {value} );".format(key=search, value=" ".join(res))
    else:
        return "{search}={value};".format(search=search, value=res)


def print_yaml(res):
    return yaml.dump(res, default_flow_style=False)


def print_json(res):
    return json.dumps(res, indent=4)


def print_toml(res):
    try:
        return toml.dumps(res)
    # (hberaud) Catch cases when only the value of a key is captured
    except AttributeError:
        return res

# niet

[![Build Status](https://travis-ci.org/gr0und-s3ct0r/niet.svg?branch=devel)](https://travis-ci.org/gr0und-s3ct0r/niet)
![PyPI](https://img.shields.io/pypi/v/niet.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niet.svg)
![PyPI - Status](https://img.shields.io/pypi/status/niet.svg)

Get data from yaml file directly in your shell

## Install or Update niet

```sh
$ pip install -U niet
```

## Requirements

- Python 2.7+

## Usage

### With YAML file

Consider the yaml file with the following content:
```yaml
# /path/to/your/file.yaml
project:
    meta:
        name: my-project
    foo: bar
    list-items:
        - item1
        - item2
        - item3
```

You can [download the previous example](https://gist.githubusercontent.com/4383/53e1599663b369f499aa28e27009f2cd/raw/389b82c19499b8cb84a464784e9c79aa25d3a9d3/file.yaml) locally for testing purpose or use the command line for this:
```shell
wget https://gist.githubusercontent.com/4383/53e1599663b369f499aa28e27009f2cd/raw/389b82c19499b8cb84a464784e9c79aa25d3a9d3/file.yaml
```

You can retrieve data from this file by using niet like this:
```sh
$ niet /path/to/your/file.yaml ".project.meta.name"
my-project
$ niet /path/to/your/file.yaml ".project.foo"
bar
$ niet /path/to/your/file.yaml ".project.list-items"
item1 item2 item3
$ # assign return value to shell variable
$ NAME=$(niet /path/to/your/file.yaml ".project.meta.name")
$ echo $NAME
my-project
```

### With JSON file

Consider the json file with the following content:
```json
{
    "project": {
        "meta": {
            "name": "my-project"
        }
    },
    "foo": "bar",
    "list-items": [
        "item1",
        "item2",
        "item3"
    ]
}
```

You can [download the previous example](https://gist.githubusercontent.com/4383/1bab8973474625de738f5f6471894322/raw/0048cd2310df2d98bf4f230ffe20da8fa615cef3/file.json) locally for testing purpose or use the command line for this:
```shell
wget https://gist.githubusercontent.com/4383/1bab8973474625de738f5f6471894322/raw/0048cd2310df2d98bf4f230ffe20da8fa615cef3/file.json
```

You can retrieve data from this file by using niet like this:
```sh
$ niet /path/to/your/file.json "project.meta.name"
my-project
$ niet /path/to/your/file.json "project.foo"
bar
$ niet /path/to/your/file.json "project.list-items"
item1 item2 item3
$ # assign return value to shell variable
$ NAME=$(niet /path/to/your/file.json "project.meta.name")
$ echo $NAME
my-project
```

### Output formats 
You can change the output format using the -f or --format optional 
argument. 

By default, niet detect the input format and display complex objects
in the same format. If the object is a list or a value, newline output
format will be used.

Output formats are: 
  - ifs
  - squote
  - dquote
  - newline
  - yaml
  - json

#### ifs
Ifs output format print all values of a list or a single value in one line.
All values are separated by the content of IFS environment variable if defined,
space otherwise.

Examples (consider the previous [YAML file example](#with-yaml-file)):
```shell
$ IFS="|" niet /path/to/your/file.yaml .project.list-items -f ifs
item1|item2|item3
$ IFS=" " niet /path/to/your/file.yaml .project.list-items -f ifs
item1 item2 item3
$ IFS="@" niet /path/to/your/file.yaml .project.list-items -f ifs
item1@item2@item3
```

This is usefull in a shell for loop,
but your content must, of course, don't contain IFS value:
```shell
OIFS="$IFS"
IFS="|"
for i in $(niet /path/to/your/file.yaml .project.list-items -f ifs); do
    echo ${i}
done
IFS="${OIFS}"
```

Previous example provide the following output:
```sh
item1
item2
item3
```

For single quoted see [squote](#squote) ouput or [dquote](#dquote) double quoted output with IFS

#### squote
Squotes output format print all values of a list or a single value in one line.
All values are quoted with single quotes and are separated by IFS value.

Examples (consider the previous [YAML file example](#with-yaml-file)):
```shell
$ # With the default IFS
$ niet /path/to/your/file.yaml .project.list-items -f squote
'item1' 'item2' 'item3'
$ # With a specified IFS
$ IFS="|" niet /path/to/your/file.yaml .project.list-items -f squote
'item1'|'item2'|'item3'
```

#### dquote
Dquotes output format print all values of a list or a single value in one line.
All values are quoted with a double quotes and are separated by IFS value.

Examples (consider the previous [YAML file example](#with-yaml-file)):
```shell
$ # With the default IFS
$ niet /path/to/your/file.yaml .project.list-items -f dquote
'item1' 'item2' 'item3'
$ # With a specified IFS
$ IFS="|" niet /path/to/your/file.yaml .project.list-items -f dquote
"item1"|"item2"|"item3"
```

#### newline
Newline output format print one value of a list or a single value per line.
This format is usefull using shell while read loop. eg:
```sh
while read value: do
    echo $value
done < $(niet --format newline your-file.json project.list-items)
```
 
#### yaml
Yaml output format force output to be in YAML regardless the input file format.

#### json
Json output format force output to be in JSON regardless the input file format.

### Deal with errors

When your JSON file content are not valid niet display an error and exit
with return code `1`

You can easily protect your script like this:
```sh
PROJECT_NAME=$(niet your-file.yaml project.meta.name)
if [ "$?" = "1" ]; then
    echo "Error occur ${PROJECT_NAME}"
else
    echo "Project name: ${PROJECT_NAME}"
fi
```

## Examples

You can try niet by using the samples provided with the project sources code.

> All the following examples use the sample file available in niet sources code
at the following location `tests/samples/sample.yaml`.

Sample example:
```yaml
# tests/samples/sample.yaml
project:
    meta:
        name: my-project
    foo: bar
    list-items:
        - item1
        - item2
        - item3
```

Retrieve the project name:
```sh
$ niet tests/samples/sample.yaml project.meta.name
my-project
```

Deal with list of items
```sh
$ for el in $(niet tests/samples/sample.yaml project.list-items); do echo ${el}; done
item1
item2
item3
```

## Tips

You can pass your search with or without quotes like this:
```sh
$ niet your-file.yaml project.meta.name
$ niet your-file.yaml "project.meta.name"
```

## Contribute

If you want to contribute to niet [please first read the contribution guidelines](CONTRIBUTING.md)

## Licence

This project is under the MIT License.

[See the license file for more details](LICENSE)

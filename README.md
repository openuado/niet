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
space otherwise. This is usefull in a shell 
for loop, but your content must, of course, don't contain IFS value.
```sh
OIFS="$IFS"
IFS="|"
for i in $(niet tests/samples/sample.yaml .project.list-items -f ifs); do
	echo $i
done
IFS="$OIFS"
```

#### squote
Squotes output format print all values of a list or a single value in one line.
All values are quoted with single quotes and are separated by IFS value.

#### dquote
Dquotes output format print all values of a list or a single value in one line.
All values are quoted with a double quotes and are separated by IFS value.

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

Sample example:
```yaml
# tests/samples/sample.yaml
project:
    meta:
        name: project-sample
        tags:
          - example
          - sample
          - for
          - testing
          - purpose
```

Retrieve the project name:
```sh
$ niet tests/samples/sample.yaml project.meta.name
project-sample
```

Deal with list of items
```sh
$ for el in $(niet tests/samples/sample.yaml project.meta.tags); do echo ${el}; done
example
sample
for
testing
purpose
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

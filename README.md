# niet

Get data from yaml file directly in your shell

## Install

```sh
$ pip install niet
```

## Usage

### With YAML file

Consider the yaml file with the following content:
```yaml
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
$ niet /path/to/your/file.yaml "project.meta.name"
my-project
$ niet /path/to/your/file.yaml "project.foo"
bar
$ niet /path/to/your/file.yaml "project.list-items"
'item1' 'item2' 'item3'
$ # assign return value to shell variable
$ NAME=$(niet /path/to/your/file.yaml "project.meta.name")
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
'item1' 'item2' 'item3'
$ # assign return value to shell variable
$ NAME=$(niet /path/to/your/file.json "project.meta.name")
$ echo $NAME
my-project
```

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

## Tips

You can pass your search with or without quotes like this:
```sh
$ niet your-file.yaml project.meta.name
$ niet your-file.yaml "project.meta.name"
```

## Tests

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

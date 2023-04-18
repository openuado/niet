CHANGES
=======

Not yet released
----------------

* [feature] the toml format is now supported by niet (https://github.com/openuado/niet/pull/77)
* [CI/CD] move away from travis CI and fix existing github actions

3.0.0
-----

* [packaging] rewrite the way we package niet and move away from pbr
* [doc] update the contribution guide

2.5.0
-----

* [fix] return key equal to False and 0 rather than raising an element not found (https://github.com/openuado/niet/issues/72)
* [requirements] bump PyYAML from version 5.1 to version 5.4.1
* [doc] improve documentation and error messages

2.4.0
-----

* fix changelog and integration badges

2.3.0
-----

* Adding a debug mode to niet
* [doc] add more examples for the `comma` format

2.2.0
-----

* [feature] adding the comma output format
* [fix] improve alignement on the help's format
* [fix] rename unit test module

2.1.0
-----

* [feature] allow niet to work on web resources (distant JSON/YAML file)

2.0
---

* drop support of python 2.7

1.8.2
-----

* fix use newline format on single value
* add download badge
* update changelog

1.8.1
-----

* fix infilename retrieve if input come from stdin
* rename Changelog
* Update Changelog

1.8.0
-----

* [feat #11] Add in-place and output function to print output to a file
* [fix #41] Remove future import
* [doc #10] Add some usecases
* [doc] Improve contributing guide to explain how to run it locally explicitly
* update doc help and options
* add features example
* Introduce some examples with eval

1.7.0
-----

* Introduce eval output

1.6.1
-----

* fix json examples structure

1.6.0
-----

* Handle jmespath lexer errors with path which contains dash
* Disable python3.8 tests on travis
* Support of python 3.8
* remove testing of python 3.5 and 3.6 development versions
* update changelog

1.5.1
-----

* Fix JSON issue when content start with a list
* compatibility with python3.7
* transfer project to openuado organization
* Introduce search by using xpath syntax
* move from devel branch to master branch as the default branch

1.4.2
-----

* fix license typo

1.4.1
-----

* Fixing list of dict extract
* fix pbr setup requirements

1.4.0
-----

* Update Changelog and fix travis automatic deployment
* get the niet version number
* document silent mode
* allow to use silent mode and doesn't display element not found
* Remove duplicate actions
* Explain how to use bandit to contributors
* Scan project code with bandit during CI

1.3.0
-----

* update changelog
* read data from stdin or from file (#25)
* introduce unittest (#7)
* improve documentation and add more examples and fix (#8)
* improve contributing
* Update changelog and authors
* Add possibility to begin search string by a point eg: .project
* Improve multiples output functionnality
* make adequation between examples in doc and functionnal tests
* Add yaml and json output format
* remove python 3.3 support
* Feat. Add capacity to choose between quotes or not
* fix pep8 and check pep8 on travis
* [feat] Add capability to get the whole file using "." as object filter
* Minor cosmetics changes
* doc explain how to update niet
* update changelog
* deploy to test.pypi.org on devel
* add some classifiers and change author email
* add badges and improve documentation
* introduce pipenv and pipfile
* add gitignore rules
* introduce tests
* how to contribute to niet
* Introduce code of conduct
* License MIT
* remove changelog from pypi description
* fix bad behavior that still to occur on not found
* fix bad behavior on element not found
* fix documentation examples
* remove tick from list results
* using readme at markdown format on pypi
* First commit

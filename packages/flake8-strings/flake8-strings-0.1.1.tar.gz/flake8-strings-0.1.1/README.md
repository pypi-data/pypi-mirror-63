# flake8-strings

[![pypi](https://badge.fury.io/py/flake8-strings.svg)](https://pypi.org/project/flake8-strings)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-strings)
[![Downloads](https://img.shields.io/pypi/dm/flake8-strings.svg)](https://pypistats.org/packages/flake8-strings)
[![Build Status](https://travis-ci.org/d1618033/flake8-strings.svg?branch=master)](https://travis-ci.org/d1618033/flake8-strings)
[![Code coverage](https://codecov.io/gh/d1618033/flake8-strings/branch/master/graph/badge.svg)](https://codecov.io/gh/d1618033/flake8-strings)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://en.wikipedia.org/wiki/MIT_License)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Description

Flake8 Linter for Strings


### Checks:


* STR001: Unnecessary use of backslash escaping 

e.g: 

Bad:

```python
path = 'C:\\Users\\root'
```

Good:

```python
path = r'C:\Users\root'
```


## Installation

    pip install flake8-strings

## Usage

`flake8 <your code>`

## For developers

### Create venv and install deps

    make init

### Install git precommit hook

    make precommit_install

### Run linters, autoformat, tests etc.

    make pretty lint test

### Bump new version

    make bump_major
    make bump_minor
    make bump_patch

## License

MIT

## Change Log

Unreleased
-----

* ...

0.1.1 - 2020-03-14
-----

* ...

0.1.0 - 2020-03-14
-----

* initial

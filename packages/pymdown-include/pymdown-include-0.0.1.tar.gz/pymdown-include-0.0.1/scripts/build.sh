#!/bin/bash

set -ex

pip install -e .

# Build README.rst
pandoc -t rst README.md  > README.rst

# Build code
python setup.py build
python setup.py sdist bdist_wheel

# Test
coverage erase
coverage run --source=pymdown_include --omit=pymdown_include/unit_tests/* -m pytest
coverage report -m

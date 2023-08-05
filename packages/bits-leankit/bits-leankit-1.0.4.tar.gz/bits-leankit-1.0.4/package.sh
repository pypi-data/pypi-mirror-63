#!/bin/sh

PACKAGE="bits_leankit"

sudo rm -rf build/ dist/ ${PACKAGE}-info/

python3 -m pip install --user --upgrade setuptools wheel

python3 setup.py sdist bdist_wheel

python3 -m pip install --user --upgrade twine

python3 -m twine upload  dist/*

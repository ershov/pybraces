#!/bin/bash

./init-pack.sh
. .venv/bin/activate
python3 setup.py sdist bdist_wheel


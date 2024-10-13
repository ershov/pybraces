#!/usr/bin/env python3

from setuptools import setup
from pybraces import PYBRACES_VERSION

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().split()

setup(
    name="pybraces",
    version=PYBRACES_VERSION,
    author="Yury Ershov",
    license="GPL3",
    description="Python with braces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ershov/pybraces",
    scripts=["bin/pyb", "bin/pybraces"],
    packages=["pybraces"],
    install_requires = requirements,
    zip_safe=False)

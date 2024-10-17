# PyBraces - Python with Braces

Python is a great language, but writing one-liners in it can be challenging.
PyBraces fixes that.

## TL;DR

`$ pyb -c 'def fn(n): { for i in range(n): { print(f"Hello World {i}"); } } fn(5);'`

```
Hello World 0
Hello World 1
Hello World 2
Hello World 3
Hello World 4
```

`$ pyb -t -c 'def fn(n): { for i in range(n): { print(f"Hello World {i}"); } } fn(5);'`

```python
def fn(n):
    for i in range(n):
        print(f"Hello World {i}")
fn(5)
```

# Installation

```bash
pip install pybraces
```

# Usage

```bash
# Transform input.b.py to output.py
$ pyb -t < input.b.py > output.py

# Transform oneliner script into Python
$ pyb -t -c 'if 1: { if 2: { print(3) } }'

# Execute oneliner script as Python
$ pyb -c 'if 1: { if 2: { print(3) } }'
$ pyb -c 'if 1: { if 2: print(3) }'
```

# Description

This package is a preprocessor that transforms Python code with braces into Python code with indentation.
Although it's targeted to writing one-liners in Python, it can be used to write Python code with braces.

The implementation is extremely lightweight and has only one dependency:
[regex](https://pypi.org/project/regex/) package for recursive regexes.
Once Python natively supports recursive regexes, the dependency will be removed.

In comparison to Bython, PyBraces doesn't require a special syntax for inline dictionaries.

The `pyb` command that comes with this package can be used to transform Python code with braces
into Python code with indentation or to directly execute code as Python.
It then passes all arguments to the Python interpreter.

## Transformation Rules

The transformation is done by the following rules:

1. `: {...}` in indented appropriately, braces are removed.
2. `: {...}` can be nested.
3. `;` inserts a newline, this terminating the statement.
5. `# comments` are removed.
6. Newlines are replaced with a space.
7. Everything inside of `[]` or `()` is pasted as is.
8. Everything else is pasted as is.

## Why semicolon?

One might ask why the semicolon is kept in the "braced" syntax?

Why
```python
if 1: { print(1) }
```
not just
```python
if 1 { print(1) }
```

This is to avoid confusion with dicts and sets where braces are used in normal Python so that
normal syntax for dicts and sets can be used with braces:

```python
a = {"qwe": 123, "asd": 456}
b = 5 in {1, 2, 3}
```

## What's the standard file extension for PyBraces?

Although one-liners are not supposed to be saved in files, the suggested extension for PyBraces is
`.b.py`. PyBraces syntax is not exactly Python but still close to it, so
developers can benefit from syntax highlighting and other features of their IDEs
to some extent.

# Links

* This project on GitHub: [PyBraces](https://github.com/ershov/pybraces)
* Prior art: [Bython](https://github.com/mathialo/bython)

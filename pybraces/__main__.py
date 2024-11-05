#!/usr/bin/env python3

import sys
import subprocess
from .pybraces import *
import regex

def _file_content(fname: str) -> str:
    try:
        with open(fname) as file:
            return file.read()
    except Exception as e:
        _err(f"{fname}: {e.strerror}")

def _stdin_content() -> str:
    try:
        return sys.stdin.read()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    except Exception as e:
        _err(f"stdin: {e.strerror}")
        sys.exit(1)

def _err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)

def add_auto_modules(txt: str) -> str:
    modules = set(regex.findall(r"\b(?:\L<names>)\b", txt,
            flags=regex.RegexFlag.V1 | regex.RegexFlag.S | regex.RegexFlag.X,
            names=[ # https://docs.python.org/3/py-modindex.html
"regex",
"__future__", "__main__", "_thread", "_tkinter", "abc", "argparse", "array", "ast", "asyncio", "atexit", "base64",
"bdb", "binascii", "bisect", "builtins", "bz2", "calendar", "cmath", "cmd", "code", "codecs", "codeop", "colorsys",
"compileall", "configparser", "contextlib", "contextvars", "copy", "copyreg", "cProfile", "csv", "ctypes", "dataclasses",
"datetime", "decimal", "difflib", "dis", "doctest", "ensurepip", "enum", "errno", "faulthandler", "filecmp",
"fileinput", "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext", "glob",
"graphlib", "gzip", "hashlib", "heapq", "hmac", "idlelib", "imaplib", "inspect", "io", "ipaddress", "itertools",
"keyword", "linecache", "locale", "lzma", "mailbox", "marshal", "math", "mimetypes", "mmap", "modulefinder", "netrc",
"numbers", "operator", "optparse", "pathlib", "pdb", "pickle", "pickletools", "pkgutil", "platform", "plistlib",
"poplib", "pprint", "profile", "pstats", "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random", "re", "reprlib",
"rlcompleter", "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "sitecustomize",
"smtplib", "socket", "socketserver", "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct",
"subprocess", "symtable", "sysconfig", "tabnanny", "tarfile", "tempfile", "textwrap", "threading", "time",
"timeit", "token", "tokenize", "tomllib", "trace", "traceback", "tracemalloc", "turtle",
"turtledemo", "types", "typing", "unicodedata", "usercustomize", "uuid", "venv", "warnings", "wave", "weakref",
"webbrowser", "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo",
            ]))
    return f"import {', '.join(modules)}\n{txt}" if modules else txt

def pybraces_main():
    extra_args = sys.argv[1:]
    args = [sys.executable]

    if not extra_args:
        args += ["-c", braces2py(_stdin_content())]
    else:
        if extra_args[0] in ["-h", "--help"]:
            print(f"""\
Python with braces version {PYBRACES_VERSION}
Usage: pyb -t [-c CODE | FILE | -]...            - convert string or file to Python.
       pyb [-M args...] [FILE] | [-c CODE] | [-] | [args...]  - execute converted code.

-t           - convert the code to python and print it to stdout.
-t FILE      - convert the code from FILE to python and print it to stdout.
-t -c CODE   - convert the code to python and print it to stdout.
               -t can be followed by multiple -c, FILE or - arguments.
               If -t is given, the program will only convert the code,
               otherwise it will run it.
               -t must be the first argument.

-c CODE [args...]  - the code to python and execute it as python, passing the remaining arguments.
FILE [args...]     - read from FILE and execute the converted code as python,
                     passing the remaining arguments to command line.
no arguments       - read from stdin and execute the converted code as python.

-M, -M*      - automatically import all standard modules found in the code.
-M MODULE    - automatically import MODULE
               ~ import MODULE
-M MODULE1,MODULE2,... - automatically import MODULE1, MODULE2, ...
               ~ import MODULE1, MODULE2, ...
-M MODULE1=ALIAS1,MODULE2=ALIAS2 - automatically import MODULE1 and MODULE2 and rename them
               ~ import MODULE as ALIAS1, MODULE2 as ALIAS2
-M MODULE:name1,name2,... - automatically import names from MODULE
               ~ from MODULE import name1, name2, ...
-M MODULE:name1=alias1,name2=alias2,... - automatically import names from MODULE and rename them.
               ~ from MODULE import name1 as alias1, name2 as alias2, ...

All other arguments are passed to the python interpreter.

Project home: https://github.com/ershov/pybraces
""", end="")
            sys.exit(0)
        if extra_args[0] == "-t":  # Print the converted code to stdout
            extra_args.pop(0)
            if not extra_args:
                print(braces2py(_stdin_content()))
                sys.exit(0)
            while extra_args:
                arg = extra_args.pop(0)
                if not arg.startswith("-"):
                    print(braces2py(_file_content(arg)))
                else:
                    if arg == "-c":
                        if extra_args:
                            print(braces2py(extra_args.pop(0)))
                        else:
                            _err(f"Option '-c' requires an argument.")
                    else:
                        _err(f"Unknown option: {arg}. '-t' can only be followed by '-c' or a file name.")
            sys.exit(0)
        auto_mods = False
        script = ""
        while extra_args:
            arg = extra_args.pop(0)
            if not arg.startswith("-"):  # read the code from a file
                script2 = braces2py(_file_content(arg))
                if auto_mods:
                    script2 = add_auto_modules(script2)
                args += ["-c", script + script2]
                break
            elif arg == "-":  # read the code from stdin
                script2 = braces2py(_stdin_content(arg))
                if auto_mods:
                    script2 = add_auto_modules(script2)
                args += ["-c", script + script2]
                break
            else:
                if arg == "-c":  # read the code from the argument
                    if extra_args:
                        script2 = braces2py(extra_args.pop(0))
                        if auto_mods:
                            script2 = add_auto_modules(script2)
                        args += ["-c", script + script2]
                        break
                    else:
                        _err(f"Option '-c' requires an argument.")
                elif arg.startswith("-M"):  # import modules
                    arg = (arg[2:]
                           if len(arg) > 2 else
                           extra_args.pop(0)
                           if extra_args and not extra_args[0].startswith("-") else
                           "")
                    if not arg:
                        auto_mods = True  # import all standard modules found in the code
                    else:
                        if (match := regex.fullmatch(r"""
                                        (?P<modname>[\w\.]++)(?P<alias>(?> = [\w\.]++)?)
                                    (?>
                                      , (?P<modname>[\w\.]++)(?P<alias>(?> = [\w\.]++)?)
                                    )*+
                                """,
                                arg,
                                flags=regex.RegexFlag.V1 | regex.RegexFlag.S | regex.RegexFlag.X)):
                            # Import modules (and rename them)
                            importslist = []
                            for i in range(0, len(match.allcaptures()[1])):
                                modname, alias = match.capturesdict()["modname"][i], match.capturesdict()["alias"][i]
                                if modname == "*":
                                    auto_mods = True
                                else:
                                    importslist.append(f"{modname} as {alias[1:]}" if alias else modname)
                            if importslist:
                                script += f"import {', '.join(importslist)}\n"
                        elif (match := regex.fullmatch(r"""
                                        (?P<modname>[\w\.]++):(?P<imports>.*)
                                """,
                                arg,
                                flags=regex.RegexFlag.V1 | regex.RegexFlag.S | regex.RegexFlag.X)):
                            # Import names from a module (and rename them)
                            modname, imports = match.capturesdict()["modname"][0], match.capturesdict()["imports"][0]
                            if (match := regex.fullmatch(r"""
                                            (?P<symbol>[\w\.]++)(?P<alias>(?> = [\w\.]++)?)
                                        (?>
                                        , (?P<symbol>[\w\.]++)(?P<alias>(?> = [\w\.]++)?)
                                        )*+
                                    """,
                                    imports,
                                    flags=regex.RegexFlag.V1 | regex.RegexFlag.S | regex.RegexFlag.X)):
                                importslist = []
                                for i in range(0, len(match.allcaptures()[1])):
                                    symbol, alias = match.capturesdict()["symbol"][i], match.capturesdict()["alias"][i]
                                    importslist.append(f"{symbol} as {alias[1:]}" if alias else symbol)
                                if importslist:
                                    script += f"from {modname} import {', '.join(importslist)}\n"
                            else:
                                _err(f"Invalid argument for -M: {arg}")
                        else:
                            _err(f"Invalid argument for -M: {arg}")
                elif arg == "--":  # Treat the next arg as a file name and read from it, stop parsing options
                    if extra_args:
                        script2 = braces2py(_file_content(extra_args.pop(0)))
                        if auto_mods:
                            script2 = add_auto_modules(script2)
                        args += ["-c", script + script2]
                    else:
                        args.append("--")
                    break
                else:
                    args.append(arg)

    # execute the converted code with the same python interpreter and computed command line arguments
    return subprocess.call(args + extra_args)

if __name__ == "__main__":
    import sys
    sys.exit(pybraces_main())

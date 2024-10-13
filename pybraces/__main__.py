#!/usr/bin/env python3

import sys
import subprocess
from .pybraces import *

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
       pyb [FILE] | [-c CODE] | [-] | [args...]  - execute converted code.

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

Project home: https://github.com/ershov/pybraces
""", end="")
            sys.exit(0)
        if extra_args[0] == "-t":
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
        while extra_args:
            arg = extra_args.pop(0)
            if not arg.startswith("-"):
                args += ["-c", braces2py(_file_content(arg))]
                break
            elif arg == "-":
                args += ["-c", braces2py(_stdin_content())]
                break
            else:
                if arg == "-c":
                    if extra_args:
                        args += ["-c", braces2py(extra_args.pop(0))]
                        break
                    else:
                        _err(f"Option '-c' requires an argument.")
                elif arg == "--":
                    if extra_args:
                        args += ["-c", braces2py(_file_content(extra_args.pop(0)))]
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

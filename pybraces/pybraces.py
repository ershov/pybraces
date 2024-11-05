#!/usr/bin/env python3

import regex

PYBRACES_VERSION = "0.2.0"

_re_pybracetoken = r'''(?(DEFINE)
    (?<TOKEN>
        (?&COMMENT) |
        (?> """ (?> [^\\"] | \\. | (?>"[^"]) | (?>""[^"]) )* """)  |
        (?> \'\'\' (?> [^\\'] | \\. | (?>'[^']) | (?>''[^']) )* \'\'\' ) |
        (?> " (?> [^\\"] | \\. )* " ) |
        (?> ' (?> [^\\'] | \\. )* ' ) |
        (?> \{ (?&DATA)*+ \} ) |
        (?> \( (?&DATA)*+ \) ) |
        (?> \[ (?&DATA)*+ \] ) |
        (?> \: (?>(?&COMMENT)|(?&SPACE))*+ \{ ) |
        (?> \} ) |
        (?> ; ) |
        (?> : ) |
        (?> \\. ) |
        (?&SPACE) |
        (?> [^\#\"\'\{\}\(\)\[\]\;\:\s\\]++)
    )
    (?<DATA>
        (?&COMMENT) |
        (?> """ (?> [^\\"] | \\. | (?>"[^"]) | (?>""[^"]) )* """)  |
        (?> \'\'\' (?> [^\\'] | \\. | (?>'[^']) | (?>''[^']) )* \'\'\' ) |
        (?> " (?> [^\\"] | \\. )* " ) |
        (?> ' (?> [^\\'] | \\. )* ' ) |
        (?> \{ (?&DATA)*+ \} ) |
        (?> \( (?&DATA)*+ \) ) |
        (?> \[ (?&DATA)*+ \] ) |
        (?> [^\#\"\'\{\}\(\)\[\]]++)
    )
    (?<COMMENT>
        (?> \# [^\n]*+ \n)
    )
    (?<SPACE>
        (?> \s++ )
    )
)''' # /nxs;

_re_flags = regex.RegexFlag.VERSION1 | regex.RegexFlag.DOTALL | regex.RegexFlag.VERBOSE

_reg_pybracetoken = regex.compile(r"(?&TOKEN)"+_re_pybracetoken, _re_flags)

def braces2py(txt: str, indent: str="    ") -> str:
    indentLevel = 0
    indentStr = ""
    eol = False
    spc: bool | None = None
    wantPass = False
    ret = []
    lastoffset = 0

    for match in _reg_pybracetoken.finditer(txt):
        if lastoffset < match.start():
            ret.append(txt[lastoffset:match.start()])
        lastoffset = match.end()
        match match[0][0]:
            case "#":  # ignore comments
                # spc = True
                continue
            case "}":
                if wantPass:
                    ret.extend(("\n", indentStr, "pass"))
                    wantPass = False
                indentLevel -= 1
                indentStr = indent * indentLevel
                eol, spc = True, None
            case ";":
                eol, spc = True, None
            case " " | "\n" | "\t" | "\r" | "\\":
                if spc is False:
                    spc = True
            case _:
                if match[0][0] == ":" and match[0][-1] == "{":
                    # if wantPass:  # it's an error but let's do our best
                    #     ret.extend(("\n", indentStr, "if 1"))
                    #     wantPass = False
                    indentLevel += 1
                    indentStr = indent * indentLevel
                    ret.append(":")
                    eol, spc, wantPass = True, None, True
                    continue
                if eol:
                    ret.extend(("\n", indentStr))
                    eol = False
                elif spc:
                    ret.append(" ")
                spc, wantPass = False, False
                ret.append(match[0].strip())
    if lastoffset < len(txt):
        ret.append(txt[lastoffset:])
    return "".join(ret)

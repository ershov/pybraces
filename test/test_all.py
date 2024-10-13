#!/usr/bin/env python3

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.chdir(os.path.dirname(__file__))

import unittest
import re
from unittest.util import _common_shorten_repr
from glob import glob
import difflib

from pybraces import *

def file_content(fname: str) -> str:
    with open(fname) as file:
        return file.read()

class TestCaseLocal(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def assertMultiLineEqualDiff(self, result, expected, msg=None, test_id=""):
        """Assert that two multi-line strings are equal."""
        if result.rstrip() != expected.rstrip():
            resultlines = result.splitlines(keepends=False)
            expectedlines = expected.splitlines(keepends=False)
            if len(resultlines) == 1 and result.strip('\r\n') == result:
                resultlines = [result + '\n']
                expectedlines = [expected + '\n']
            standardMsg = '%s != %s' % _common_shorten_repr(result, expected)
            diff = '\n' + '\n'.join(difflib.unified_diff(expectedlines, resultlines))
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.fail(test_id+"\n"+self._formatMessage(msg, standardMsg))

    def checkFile(self, fname):
        fname = re.sub(r"\..*+$", "", fname)
        result = braces2py(file_content(f"{fname}.b.py"))
        with open(f"{fname}.test", "w") as f:
            f.write(result)
        self.assertMultiLineEqualDiff(result, file_content(f"{fname}.py"), test_id=fname)

class TestAll(TestCaseLocal):
    def test_all(self):
        for f in glob("data/*.b.py"):
            self.checkFile(f)


# Enable to run as a standalone script
if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.TestLoader().discover(os.path.dirname(__file__)))


import unittest
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pytest

import mccabe
from mccabe import get_code_complexity


# Snippets are put outside of testcases because of spacing issue that would
# otherwise occur with triple quoted strings.
trivial = 'def f(): pass'


sequential = """\
def f(n):
    k = n + 4
    s = k + n
    return s
"""


sequential_unencapsulated = """\
k = 2 + 4
s = k + 3
"""


if_elif_else_dead_path = """\
def f(n):
    if n > 3:
        return "bigger than three"
    elif n > 4:
        return "is never executed"
    else:
        return "smaller than or equal to three"
"""


for_loop = """\
def f():
    for i in range(10):
        print(i)
"""


for_else = """\
def f(mylist):
    for i in mylist:
        print(i)
    else:
        print(None)
"""


recursive = """\
def f(n):
    if n > 4:
        return f(n - 1)
    else:
        return n
"""


nested_functions = """\
def a():
    def b():
        def c():
            pass
        c()
    b()
"""

try_else = """\
try:
    print(1)
except TypeA:
    print(2)
except TypeB:
    print(3)
else:
    print(4)
"""

async_keywords = """\
async def foobar(a, b, c):
    await whatever(a, b, c)
    if await b:
        pass

    async with c:
        pass

    async for x in a:
        pass
"""


def get_complexity_number(snippet, strio, max=0):
    """Get the complexity number from the printed string."""
    # Report from the lowest complexity number.
    get_code_complexity(snippet, max)
    strio_val = strio.getvalue()
    if strio_val:
        return int(strio_val.split()[-1].strip("()"))
    else:
        return None


class McCabeTestCase(unittest.TestCase):
    def setUp(self):
        # If not assigned to sys.stdout then getvalue() won't capture anything.
        self._orig_stdout = sys.stdout
        sys.stdout = self.strio = StringIO()

    def tearDown(self):
        # https://mail.python.org/pipermail/tutor/2012-January/088031.html
        self.strio.close()
        sys.stdout = self._orig_stdout

    def assert_complexity(self, snippet, max):
        complexity = get_complexity_number(snippet, self.strio)
        self.assertEqual(complexity, max)

        # should have the same complexity when inside a function as well.
        infunc = 'def f():\n    ' + snippet.replace('\n', '\n    ')
        complexity = get_complexity_number(infunc, self.strio)
        self.assertEqual(complexity, max)

    def test_print_message(self):
        get_code_complexity(sequential, 0)
        printed_message = self.strio.getvalue()
        self.assertEqual(printed_message,
                         "stdin:1:1: C901 'f' is too complex (1)\n")

    def test_sequential_snippet(self):
        complexity = get_complexity_number(sequential, self.strio)
        self.assertEqual(complexity, 1)

    def test_sequential_unencapsulated_snippet(self):
        complexity = get_complexity_number(sequential_unencapsulated,
                                           self.strio)
        self.assertEqual(complexity, None)

    def test_if_elif_else_dead_path_snippet(self):
        complexity = get_complexity_number(if_elif_else_dead_path, self.strio)
        # Paths that will never be executed are counted!
        self.assertEqual(complexity, 3)

    def test_for_loop_snippet(self):
        complexity = get_complexity_number(for_loop, self.strio)
        # The for loop adds an execution path; sometimes it won't be run.
        self.assertEqual(complexity, 2)

    def test_for_else_snippet(self):
        complexity = get_complexity_number(for_else, self.strio)
        # The for loop doesn't add an execution path, but its `else` does
        self.assertEqual(complexity, 2)

    def test_recursive_snippet(self):
        complexity = get_complexity_number(recursive, self.strio)
        self.assertEqual(complexity, 2)

    def test_nested_functions_snippet(self):
        complexity = get_complexity_number(nested_functions, self.strio)
        self.assertEqual(complexity, 3)

    def test_trivial(self):
        """The most-trivial program should pass a max-complexity=1 test"""
        complexity = get_complexity_number(trivial, self.strio, max=1)
        self.assertEqual(complexity, None)
        printed_message = self.strio.getvalue()
        self.assertEqual(printed_message, "")

    def test_try_else(self):
        self.assert_complexity(try_else, 4)

    @pytest.mark.skipif(sys.version_info < (3, 5),
                        reason="Async keywords are only valid on Python 3.5+")
    def test_async_keywords(self):
        """Validate that we properly process async keyword usage."""
        complexity = get_complexity_number(async_keywords, self.strio)
        self.assertEqual(complexity, 3)


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.original_complexity = mccabe.McCabeChecker.max_complexity

    def tearDown(self):
        mccabe.McCabeChecker.max_complexity = self.original_complexity

    def test_max_complexity_is_always_an_int(self):
        """Ensure bug #32 does not regress."""
        class _options(object):
            max_complexity = None

        options = _options()
        options.max_complexity = '16'

        self.assertEqual(0, mccabe.McCabeChecker.max_complexity)
        mccabe.McCabeChecker.parse_options(options)
        self.assertEqual(16, mccabe.McCabeChecker.max_complexity)


if __name__ == "__main__":
    unittest.main()

# -*- encoding: utf-8 -*-
import unittest

import niet.output


class TestPrintFunctions(unittest.TestCase):
    def test_squotes(self):
        output = niet.output.print_squote(["test1", "test2"])
        self.assertEqual("'test1' 'test2'", output)

    def test_dquotes(self):
        output = niet.output.print_dquote(["test1", "test2"])
        self.assertEqual('"test1" "test2"', output)

    def test_newline(self):
        output = niet.output.print_newline(["test1", "test2"])
        self.assertEqual("test1\ntest2", output)
        output = niet.output.print_newline([1, 2])
        self.assertEqual("1\n2", output)

    def test_comma(self):
        output = niet.output.print_comma(["test1", "test2"])
        self.assertEqual("test1,test2", output)
        output = niet.output.print_comma([1, 2])
        self.assertEqual("1,2", output)

# -*- encoding: utf-8 -*-
import unittest

import niet


class TestPrintFunction(unittest.TestCase):
    def test_squotes(self):
        output = niet.out_print_squote(['test1', 'test2'])
        self.assertEqual("'test1' 'test2'", output)

    def test_dquotes(self):
        output = niet.out_print_dquote(['test1', 'test2'])
        self.assertEqual('"test1" "test2"', output)

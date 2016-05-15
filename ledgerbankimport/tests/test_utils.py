# -*- coding: utf8 -*-


import unittest

from ledgerbankimport.utils import unquote


class TestUnquote(unittest.TestCase):
    """
    Unit tests for :py:func:`ledgerbankexport.utils.unquote`.
    """

    def test_null(self):
        self.assertEqual(unquote(""), "")

    def test_negative_simple(self):
        base_input = "foobar"
        self.assertEqual(unquote(base_input), base_input)
        self.assertEqual(unquote(base_input + '"'), base_input + '"')
        self.assertEqual(unquote('"' + base_input), '"' + base_input)

    def test_negative_mixed(self):
        base_input = "foobar"
        mixed_1 = "'{}\"".format(base_input)
        self.assertEqual(unquote(mixed_1), mixed_1)
        mixed_2 = "\"{}'".format(base_input)
        self.assertEqual(unquote(mixed_2), mixed_2)

    def test_quote(self):
        base_input = "foobar"
        self.assertEqual(unquote("'{}'".format(base_input), quotechar="'"), base_input)
        self.assertEqual(unquote('"{}"'.format(base_input), quotechar='"'), base_input)

    def test_quote_strip(self):
        base_input = "foobar"
        self.assertEqual(unquote("'  {}  '".format(base_input), quotechar="'"), base_input)
        self.assertEqual(unquote('"  {}  "'.format(base_input), quotechar='"'), base_input)

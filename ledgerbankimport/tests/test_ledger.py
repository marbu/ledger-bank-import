# -*- coding: utf8 -*-

# Copyright (C) 2016 martin.bukatovic@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
import textwrap

from ledgerbankimport.ledger import Transaction, LedgerError, export_posting


class TestTransactionFirstLine(unittest.TestCase):

    def test_firstline_simple(self):
        t1 = Transaction("2010-09-15", "test")
        self.assertEqual(t1.export_firstline(), "2010-09-15 test")

    def test_firstline_edate(self):
        t1 = Transaction("2010-09-15", "test", edate="2010-09-17")
        self.assertEqual(t1.export_firstline(), "2010-09-15=2010-09-17 test")

    def test_firstline_cleared(self):
        t1 = Transaction("2010-09-15", "test", cleared=True)
        self.assertEqual(t1.export_firstline(), "2010-09-15 * test")

    def test_firstline_pending(self):
        t1 = Transaction("2010-09-15", "test", pending=True)
        self.assertEqual(t1.export_firstline(), "2010-09-15 ! test")

    def test_firstline_code(self):
        t1 = Transaction("2010-09-15", "test", code=42)
        self.assertEqual(t1.export_firstline(), "2010-09-15 (42) test")

    def test_firstline_full(self):
        t1 = Transaction(
            "2010-09-15", "description of a test transaction",
            edate="2010-09-17", pending=True, code=142)
        t2 = Transaction(
            "2010-09-15", "description of a test transaction",
            edate="2010-09-17", pending=False, code=127)
        self.assertEqual(
            t1.export_firstline(),
            "2010-09-15=2010-09-17 ! (142) description of a test transaction")
        self.assertEqual(
            t2.export_firstline(),
            "2010-09-15=2010-09-17 (127) description of a test transaction")


class TestTransactionPosting(unittest.TestCase):

    def test_posting_null(self):
        with self.assertRaises(LedgerError):
            export_posting({})

    def test_posting_simple(self):
        posting = {'account': 'expenses:food'}
        str_exp = "    expenses:food"
        self.assertEqual(export_posting(posting), str_exp)

    def test_posting_amount_nounit(self):
        posting = {'account': 'expenses:food', 'amount': 100}
        with self.assertRaises(LedgerError):
            export_posting(posting)

    def test_posting_amount_simple(self):
        posting = {'account': 'expenses:food', 'amount': 100, 'unit': 'CZK'}
        str_exp = "    expenses:food \t\t100 CZK"
        self.assertEqual(export_posting(posting), str_exp)

    def test_posting_amount_total(self):
        posting = {
            'account': 'expenses:food',
            'amount': 100,
            'unit': 'CZK',
            'total': 5201,
            }
        str_exp = "    expenses:food \t\t100 CZK = 5201 CZK"
        self.assertEqual(export_posting(posting), str_exp)

    def test_posting_amount_note(self):
        posting = {
            'account': 'expenses:food',
            'amount': 100,
            'unit': 'CZK',
            'note': 'foobar',
            }
        str_exp = "    expenses:food \t\t100 CZK ; foobar"
        self.assertEqual(export_posting(posting), str_exp)


class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.t1 = Transaction("2010-09-15", "test")

    def test_init(self):
        t2 = Transaction("2010-09-15", "test", cleared=True)
        t3 = Transaction("2010-09-15", "test", pending=True)
        with self.assertRaises(LedgerError):
            t4 = Transaction("2010-09-15", "test", cleared=True, pending=True)

    def test_str(self):
        self.assertEqual(str(self.t1), "Transaction 2010-09-15 test")

    def test_export_null(self):
        expected = textwrap.dedent("""\
        2010-09-15 test
        """)
        self.assertEqual(self.t1.export(), expected)

    def test_export_single_simple(self):
        self.t1.add_posting("expenses:food", 10, unit='EUR')
        expected = textwrap.dedent("""\
        2010-09-15 test
            expenses:food \t\t10 EUR
        """)
        self.assertEqual(self.t1.export(), expected)

    def test_export_single(self):
        self.t1.add_posting("expenses:food", 10, unit='EUR')
        self.t1.add_posting("assets:checking")
        expected = textwrap.dedent("""\
        2010-09-15 test
            expenses:food \t\t10 EUR
            assets:checking
        """)
        self.assertEqual(self.t1.export(), expected)

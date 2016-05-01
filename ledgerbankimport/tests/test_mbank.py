# -*- coding: utf8 -*-


import unittest
from io import StringIO

from ledgerbankimport.bank import mbank


# TODO: currently broken, make it work (StopIteration issue)

class TestBase(unittest.TestCase):

    def setUp(self):
        """
        Prepare metadata header for minimal input file.
        """
        # so far the only mandatory header: self acct number
        self.acct = "670100-0123456789/6210"
        header = "#Číslo účtu:\n{acct};\n\n".format(acct=self.acct)
        # create virtual file from string, encoded in cp1250
        self.in_file = StringIO(header.encode("cp1250"))

    def tearDown(self):
        self.in_file.close()

    def assertEntryEqual(self, in_entry, ledger_entry, msg):
        """
        Check convertion of single ledger entry.
        """
        self.in_file.write(in_entry.encode("cp1250") + "\n")
        result_entry = mbank.bank_import(self.in_file).next()
        self.assertEqual(ledger_entry, result_entry, msg)

    def test_example(self):
        """
        An example of a test.
        """
        in_entry = '''15-09-2010;15-09-2010;ODCHOZÍ PLATBA DO MBANK;"0000000000";"JAN NOVAK";'670100-1111111111/6210';;;;-3 000,00;22 098,00;'''
        ledger_entry = (
            "2010-09-15 ODCHOZÍ PLATBA DO MBANK\n"
            "    ; name: JAN NOVAK\n"
            "    ; msg: 0000000000\n"
            "    acct:{acct}  -3000.00 CZK = 22098.00 CZK\n"
            "    acct:670100-1111111111/6210\n\n").format(acct=self.acct)
        msg = "simple entry"
        self.assertEntryEqual(in_entry, ledger_entry, msg)

# -*- coding: utf8 -*-

"""
ledger-bank-import: converter of csv banking logs into ledger-cli format
"""

# Copyright (C) 2014  martin.bukatovic@gmail.com
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


import sys
from optparse import OptionParser
from configparser import SafeConfigParser

from ledgerbankimport.bank import mbank


def bank_import(bank_type, inputfile, debug):
    """
    Convert input file into ledger and print the result into stdout.
    """
    for ledger_entry in bank_type.bank_import(inputfile, debug):
        print(ledger_entry)

def main():
    opt_parser = OptionParser(usage="usage: %prog [options] [files]")
    opt_parser.add_option("-d", "--debug",
        action="store_true",
        help="debug mode")
    opts, args = opt_parser.parse_args()

    bank_type = mbank

    if len(args) == 0:
        bank_import(bank_type, sys.stdin, opts.debug)
        return
    for filename in args:
        with open(filename, "rb") as inputfile:
            bank_import(bank_type, inputfile, opts.debug)

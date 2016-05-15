# -*- coding: utf8 -*-

"""
ledger-bank-import: converter of bank export files into ledger-cli format
"""

# Copyright (C) 2014 martin.bukatovic@gmail.com
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


from configparser import SafeConfigParser
import argparse
import sys

from ledgerbankimport.bank import mbank


def get_banktype_module(bank_type):
    """
    Import and return module for given bank export file type.
    """
    # TODO: actually implement this
    return mbank

def import_file(bank_type, inputfile, debug):
    """
    Convert input file into ledger and print the result into stdout.
    """
    for ledger_entry in bank_type.bank_import(inputfile, debug):
        print(ledger_entry)

def main():
    parser = argparse.ArgumentParser(
        description='convert bank export files into ledger-cli format')
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="enable debug mode")
    parser.add_argument(
        "-o",
        action="store",
        required=False,
        metavar="FILE",
        help="filename of output ledger-cli file (stdout used by default)")
    parser.add_argument(
        "-t", "--type",
        action="store",
        default="mbank",
        help="type of bank export file")
    parser.add_argument(
        "exportfile",
        nargs='?',
        help="filename of a bank export file")
    args = parser.parse_args()

    # TODO: error checking
    bank_type = get_banktype_module(args.type)

    if args.exportfile is None:
        import_file(bank_type, sys.stdin, args.debug)
        return
    with open(args.exportfile, "r", encoding=bank_type.ENCODING) as inputfile:
        import_file(bank_type, inputfile, args.debug)

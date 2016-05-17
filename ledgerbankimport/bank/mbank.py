# -*- coding: utf8 -*-

"""
Import module for mBank.cz csv file format.
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


import csv
import sys

from ledgerbankimport.ledger import Transaction
from ledgerbankimport.utils import unquote


ENCODING = "cp1250"
"""
Encoding of pristine mbank export csv file.
"""

CSV_FIELDS = {
    '#Datum uskutečnění transakce': 0,
    '#Datum zaúčtování transakce': 1,
    '#Popis transakce': 2,
    '#Zpráva pro příjemce': 3,
    '#Plátce/Příjemce': 4,
    '#Číslo účtu plátce/příjemce': 5,
    '#KS': 6,
    '#VS': 7,
    '#SS': 8,
    '#Částka transakce': 9,
    '#Účetní zůstatek po transakci': 10,
    '': 11,
    }
"""
Dict of expected fields in mbank cvs transaction entires.
"""

def fix_date(rawdata):
    """
    Fix dateformat: dd-mm-yyyy -> yyyy-mm-dd
    """
    return "-".join(rawdata.split("-")[::-1])

def fix_money(rawdata):
    return rawdata.replace(" ", "").replace(",", ".")

def create_entry(row, acc_meta):
    """
    Create ledger entry object based on given raw row.
    """
    print(row, file=sys.stderr)
    date = fix_date(row[CSV_FIELDS['#Datum uskutečnění transakce']])
    desc = row[CSV_FIELDS['#Popis transakce']]
    tr = Transaction(date, desc)
    amount = fix_money(row[CSV_FIELDS['#Částka transakce']])
    tr.add_posting(acc_meta['number'], amount, unit=acc_meta['currency'])
    tr.add_posting('foo')
    # TODO:
    # for colname in (3, 4): row[col] = unquote(row[col])
    return tr

def bank_import(csvfile, debug=False):
    """
    Process mbank export csv file.
    """
    csv_reader = csv.reader(csvfile, delimiter=";", quotechar="'")
    # account metada required for exporting into ledger-cli format
    acc_meta = {}
    for row in csv_reader:
        if len(row) == 0:
            continue
        if len(row) < len(CSV_FIELDS):
            if row[0] == "#Číslo účtu:":
                acc_meta['number'] = next(csv_reader)[0]
            elif row[0] == "#Měna účtu:":
                acc_meta['currency'] = next(csv_reader)[0]
            elif row[0] == "#Typ účtu:":
                acc_meta['type'] = next(csv_reader)[0]
            continue
        if len(row) != len(CSV_FIELDS):
            continue
        # check list of all fields
        if row[0].startswith('#'):
            # TODO: format check exception, possible to disable
            continue
        # finally process data in the row
        yield create_entry(row, acc_meta)

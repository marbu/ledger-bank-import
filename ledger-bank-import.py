#!/usr/bin/env python2
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
import csv
from optparse import OptionParser
from ConfigParser import SafeConfigParser


# TODO: polish current mbank template
# TODO: move import code into dedicated module, add examples and tests
# TODO: create more import modules (fio, mbank, kb, ...)


def unquote(str_value, quotechar='"'):
    """
    Remove quotes around given string + stripping.
    """
    result = str_value
    if str_value.startswith(quotechar) and str_value.endswith(quotechar):
        result = str_value[1:-1].strip()
    return result

def preprocess_row(row, reader, metadata):
    """
    Proprocess raw row from csv file: cleanse it and try to read metadata
    """
    # convert the row into unicode
    row = { key: entry.decode("cp1250") for key, entry in row.iteritems()
        if isinstance(entry, basestring) }
    # try to read metadata
    if len(row) != 11:
        if row["date1"] == u"#Číslo účtu:":
            metadata["acct_self"] = reader.next()["date1"]
        else:
            return None
    # ignore comments
    if len(row) > 0 and row["date1"].startswith("#"):
        return None
    # hack: ignore null entries
    if row["amount"] == "0,00":
        return None
    # fix dateformat: dd-mm-yyyy -> yyyy-mm-dd
    for colname in ("date1", "date2"):
        row[colname] = "-".join(row[colname].split("-")[::-1])
    # fix money format
    for colname in ("amount", "total"):
        row[colname] = row[colname].replace(" ","").replace(",", ".")
    # remove unnecessary quoting
    for colname in ("msg", "name"):
        row[colname] = unquote(row[colname])
    return row

def get_ledger_entry(entry, metadata):
    """
    Create ledger representation for given entry.
    """
    if entry["date1"] == entry["date2"]:
        entry_header = u"{date1} {desc}"
    else:
        entry_header = u"{date1}={date2} {desc}"
    # account number
    if entry["acct"] == "" and entry["desc"] == u"VÝBĚR Z BANKOMATU":
        acct_number = u"    cash"
    elif entry["acct"] == "":
        acct_number = u"    bank"
    else:
        acct_number = u"    acct:{acct}"
    template_list = [
        entry_header,
        u"    acct:{acct_self}  {amount} CZK = {total} CZK",
        acct_number,
        u""]
    optional_fields = [
        ("ks", u"    ; ks: {ks}"),
        ("vs", u"    ; vs: {vs}"),
        ("ss", u"    ; ss: {ss}"),
        ("msg", u"    ; msg: {msg}"),
        ("name", u"    ; name: {name}"),
        ]
    for f_name, f_template in optional_fields:
        if f_name in entry and len(entry[f_name]) > 0:
            template_list.insert(1, f_template)
    # add usefull metadata into entry
    entry["acct_self"] = metadata["acct_self"]
    # fill out template and convert the result into utf8
    return u"\n".join(template_list).format(**entry).encode('utf8')

def bank_import(csvfile, debug=False):
    """
    Process (just opened) bank file.
    """
    reader = csv.DictReader(csvfile, delimiter=";", quotechar="'",
        fieldnames=[
        "date1",  # Datum uskutečnění transakce
        "date2",  # Datum zaúčtování transakce
        "desc",   # Popis transakce
        "msg",    # Zpráva pro příjemce
        "name",   # Plátce/Příjemce
        "acct",   # Číslo účtu plátce/příjemce
        "ks",
        "vs",
        "ss",
        "amount", # Částka transakce
        "total",  # Účetní zůstatek po transakci
        ])
    metadata = {}
    for row in reader:
        row = preprocess_row(row, reader, metadata)
        if row is not None:
            print get_ledger_entry(row, metadata)


def main():
    opt_parser = OptionParser(usage="usage: %prog [options] [files]")
    opt_parser.add_option("-d", "--debug",
        action="store_true",
        help="debug mode")
    opts, args = opt_parser.parse_args()

    # TODO: bank type selection

    if len(args) == 0:
        bank_import(csvfile=sys.stdin, debug=opts.debug)
        return
    for filename in args:
        with open(filename, "rb") as csvfile:
            bank_import(csvfile, debug=opts.debug)

if __name__ == '__main__':
    sys.exit(main())

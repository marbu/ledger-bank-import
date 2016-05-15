# -*- coding: utf8 -*-

"""
Module with ledger-cli export functionality.

It follow the text representation of a transaction as described by
`ledger documentation`_::

    DATE[=EDATE] [*|!] [(CODE)] DESC
          ACCOUNT  AMOUNT  [; NOTE]
          ACCOUNT  AMOUNT  [; NOTE]
          ...
          ; TAG_NAME: TAG_VALUE

.. _`ledger documentation`: http://ledger-cli.org/3.0/doc/ledger3.html#Transactions-and-Comments
"""

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


class LedgerError(Exception):
    pass


def export_posting(posting_dict):
    """
    Generate text representation of a posting of a ledger transaction.

    This method follows upstream syntax::

        ACCOUNT  [AMOUNT UNIT] [= TOTAL UNIT] [; NOTE]
    """
    items = ['   ']
    # the only mandatory field: account
    if posting_dict.get("account") is None:
        msg = "posing is missing the account information"
        raise LedgerError(msg)
    items.append('{account}')
    # unit field is mandatory only if amount and/or total is present
    if ('amount' in posting_dict or 'total' in posting_dict) \
        and 'unit' not in posting_dict:
        msg = "unit filed is missing in the posting"
        raise LedgerError(msg)
    # amount field
    if posting_dict.get("amount") is not None:
        items.append('\t\t{amount} {unit}')
    # total field
    # TODO: check if total field requires amount
    if posting_dict.get("total") is not None:
        items.append('= {total} {unit}')
    # TODO: add payee support?
    if posting_dict.get("note") is not None:
        items.append('; {note}')
    template = " ".join(items)
    return template.format(**posting_dict)


class Transaction(object):
    """
    Single ledger-cli transaction entry.
    """

    def __init__(self,
            date, desc, edate=None, cleared=False, pending=False, code=None):
        self.date = date
        self.desc = desc
        self.edate = edate
        if pending and cleared:
            msg = "Transaction can't be both pending and cleared"
            raise LedgerError(msg)
        self.cleared = cleared
        self.pending = pending
        self.code = code
        self._tags = {}
        self._posting_list = []

    def add_tag(self, name, value=None):
        self._tags[name] = value

    def add_posting(self,
        account, amount=None, unit=None, total=None, note=None):
        posting = {
            "account": account,
            "amount": amount,
            "unit": unit,
            "total": total,
            "note": note,
            }
        self._posting_list.append(posting)

    def export_firstline(self):
        """
        Generate text representation of 1st line of this transaction.

        This method follows upstream syntax::

            DATE[=EDATE] [*|!] [(CODE)] DESC
        """
        items = []
        if self.edate is not None:
            items.append("{0}={1}".format(self.date, self.edate))
        else:
            items.append("{0}".format(self.date))
        if self.cleared:
            items.append("*")
        elif self.pending:
            items.append("!")
        if self.code is not None:
            items.append("({0})".format(self.code))
        items.append(self.desc)
        return " ".join(items)

    def export(self):
        """
        Export this transaction into ledger-cli formated string.
        """
        lines = [self.export_firstline()]
        for ps in self._posting_list:
            lines.append(export_posting(ps))
        lines.append('')
        return "\n".join(lines)

    def __str__(self):
        return "Transaction " + self.export_firstline()

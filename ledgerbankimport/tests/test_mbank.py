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

from ledgerbankimport.bank import mbank


class TestCsvFields(unittest.TestCase):

    def test_index_uniqueness(self):
        csv_index_list = sorted(mbank.CSV_FIELDS.values())
        exp_index_list = list(range(0, len(mbank.CSV_FIELDS)))
        self.assertEqual(csv_index_list, exp_index_list)


class TestDataCleansing(unittest.TestCase):

    def test_fix_date(self):
        self.assertEqual(mbank.fix_date("15-03-2006"), "2006-03-15")
        self.assertEqual(mbank.fix_date("01-12-2015"), "2015-12-01")

    def test_fix_money(self):
        self.assertEqual(mbank.fix_money("-3 000,00"), "-3000.00")
        self.assertEqual(mbank.fix_money(" 5 000,77"), "5000.77")


class TestCreateEntry(unittest.TestCase):

    def test_null(self):
        # TODO
        pass

import os
from unittest import TestCase

from fabriek.csv_convert import sort, event
from fabriek.csv_convert.date_util import datum_naar_nederlandse_tekst
from settings import LOCATION
from tests.src import util


class TestDateUtil(TestCase):

    def test_datum_naar_nederlandse_tekst_none(self):
        datum_tekst = datum_naar_nederlandse_tekst(None)
        self.assertEqual(datum_tekst, None)

    def test_datum_naar_nederlandse_tekst_lege_string(self):
        datum_tekst = datum_naar_nederlandse_tekst("")
        self.assertEqual(datum_tekst, None)

    def test_datum_naar_nederlandse_tekst_spaces(self):
        datum_tekst = datum_naar_nederlandse_tekst("   ")
        self.assertEqual(datum_tekst, None)

    def test_datum_naar_nederlandse_tekst_invalid_date(self):
        with self.assertRaises(ValueError):
            datum_naar_nederlandse_tekst("2024-13-1")

    def test_datum_naar_nederlandse_tekst_ok(self):
        self.assertEqual(datum_naar_nederlandse_tekst('2024-01-01'), '1 januari 2024')
        self.assertEqual(datum_naar_nederlandse_tekst('2024-02-29'), '29 februari 2024')

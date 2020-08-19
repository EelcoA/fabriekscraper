import io
import os
from unittest import TestCase

from fabriek.csv_convert import sort
from tests.src import util

header_in = 'datum,tijd,titel,taal,genre,speelduur,cast,synopsis,beschrijving,ticket-url,film-url'
row_1_in = '2020-08-19,20:00,Berlin Alexanderplatz,"Duits, Engels",drama,183 min,' \
           '"Welket Bungué, Jella Haase, Martin Wuttke, Albrecht Schuch, Nils Verkooijen",,' \
           '"<p>Vluchteling Francis, maakt de gevaarlijke oversteek van Afrika naar Europa.",' \
           'https://tickets.de-fabriek.nl/fabriek/nl/flow_configs/webshop/steps/start/show/455853,' \
           'https://www.de-fabriek.nl/films/409-berlin+alexanderplatz.html'

row_2_in = '2020-08-19,15:15,"The Kingmaker, Imelda Marcos",Engels,documentaire,101 min,Imelda Marcos,' \
           '"Voormalig first lady van de Filipijnen, Imelda Marcos staat in ieders geheugen gegrift ",' \
           '"Voormalig first lady van de Filipijnen, Imelda Marcos staat in ieders geheugen gegrift ' \
           'als de vrouw met de vele schoenen.",' \
           'https://tickets.de-fabriek.nl/fabriek/nl/flow_configs/webshop/steps/start/show/455863,' \
           'https://www.de-fabriek.nl/films/300-the+kingmaker+imelda+marcos.html'


class TestSortCrawlData(TestCase):

    def test_sort_crawl_output_into_new_file(self):
        test_data = util.TestData(header_in, row_1_in, row_2_in)
        test_input_file = util.create_test_file("temp_file_for_sort_test.csv", test_data)

        test_output_file: io.StringIO = util.create_in_memory_test_output_file()

        sort.sort_crawl_data_into_new_file(test_input_file, test_output_file)

        rows = util.get_rows_from_test_output(test_output_file)
        header_out = rows[0]
        row_1_out = rows[1]
        row_2_out = rows[2]

        self.assertEqual(header_in, header_out)
        self.assertEqual(row_1_in, row_2_out)
        self.assertEqual(row_2_in, row_1_out)

        os.remove(test_input_file.name)

    def test_encoding_issues_step_1_sort_file_with(self):
        '''
        There were some issues with the encoding, after some research, adding 'utf-8' to the opening of
        input and output solved this issue. These test were used for that.
        '''
        input_file = util.open_test_file_for_input("fabriek_2020-08-03_134658_01_encoding.csv")
        output_file = util.open_test_file_for_output("fabriek_2020-08-03_134658_01_encoding_sorted.csv")
        sort.sort_crawl_data_into_new_file(input_file=input_file, output_file=output_file)

    def test_encoding_issues_step_1_create_event_manager_file(self):
        input_file = util.open_test_file_for_input("fabriek_2020-08-03_134658_02_encoding_sorted.csv")
        output_file = util.open_test_file_for_output("fabriek_2020-08-03_134658_03_encoding_event_manager.csv")
        sort.sort_crawl_data_into_new_file(input_file=input_file, output_file=output_file)

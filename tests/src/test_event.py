import os
from unittest import TestCase

from fabriek.csv_convert import sort, event
from tests.src import util


class Test(TestCase):
    maxDiff = None

    def test_create_event_manager_file(self):
        test_data = util.TestData(header_in, row_1_in)
        test_input_file = util.create_test_file("temp_file_for_event_manager_test.csv", test_data)

        test_output_file = util.create_in_memory_test_output_file()

        event.create_event_manager_file(test_input_file, test_output_file)

        rows = util.get_rows_from_test_output(test_output_file)
        header_out = rows[0]
        row_1_out = rows[1]

        header_row_expected = ",".join(event.event_data_header_row)

        self.assertEqual(header_row_expected, header_out)
        self.assertEqual(row_1_out_expected, row_1_out)

        os.remove(test_input_file.name)


header_in = 'datum,tijd,titel,taal,genre,speelduur,cast,synopsis,beschrijving,ticket-url,film-url'
row_1_in =           '2020-08-19,' \
                     '20:00,' \
                     'Berlin Alexanderplatz,' \
                     '"Duits, Engels",' \
                     'drama,' \
                     '183 min,' \
                     '"Welket Bungué, Jella Haase, Martin Wuttke, Albrecht Schuch, Nils Verkooijen",' \
                     'De korte samenvatting.,' \
                     '"   De korte samenvatting.  <p>   Vluchteling Francis, maakt de gevaarlijke oversteek van Afrika naar Europa.",' \
                     'https://tickets.de-fabriek.nl/fabriek/nl/flow_configs/webshop/steps/start/show/455853,' \
                     'https://www.de-fabriek.nl/films/409-berlin+alexanderplatz.html'

row_1_out_expected = '2020-08-19,' \
                     '20:00:00,' \
                     '2020-08-19,' \
                     '23:13:00,' \
                     'Berlin Alexanderplatz,' \
                     'De korte samenvatting.,' \
                     '"   De korte samenvatting.  <p>   Vluchteling Francis, maakt de gevaarlijke oversteek van Afrika ' \
                     'naar Europa.<br><br>' \
                     '<strong>Gesproken taal: </strong>Duits, Engels<br>' \
                     '<strong>Genre: </strong>drama<br>' \
                     '<strong>Speelduur: </strong>183 min<br>' \
                     '<strong>Cast: </strong>Welket Bungué, Jella Haase, Martin Wuttke, Albrecht Schuch, Nils Verkooijen<br>' \
                     '<br>' \
                     '<a href=\'https://www.de-fabriek.nl/films/409-berlin+alexanderplatz.html\'>' \
                        'https://www.de-fabriek.nl/films/409-berlin+alexanderplatz.html' \
                     '</a>",' \
                     'filmtheater-de-fabriek-2,' \
                     'film'
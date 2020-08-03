import os
from datetime import datetime
from typing import Dict, List
from unittest import TestCase

from fabriek.spiders import fabriek_helper as fh


class Test(TestCase):

    def test_to_strong(self):
        # valid
        result = fh.to_strong("Testing 1,2,3")
        expected = "<strong>Testing 1,2,3</strong>"
        self.assertEqual(result, expected)

        # None
        result = fh.to_strong(None)
        expected = None
        self.assertEqual(result, expected)

        # empty string
        result = fh.to_strong("")
        expected = ""
        self.assertEqual(result, expected)

        # just spaces
        result = fh.to_strong("  ")
        expected = ""
        self.assertEqual(result, expected)

    def test_is_invalid_begintime(self):
        # Valid
        self.assertTrue(fh.is_valid_begintijd("13:00"))

        # Invalid
        self.assertFalse(fh.is_valid_begintijd("13:00:00"))
        self.assertFalse(fh.is_valid_begintijd("130000"))
        self.assertFalse(fh.is_valid_begintijd("x13:00"))
        self.assertFalse(fh.is_valid_begintijd("13:001"))
        self.assertFalse(fh.is_valid_begintijd(None))
        self.assertFalse(fh.is_valid_begintijd(""))

    def test_is_speelduur_valid(self):
        # Valid values
        self.assertTrue(fh.is_valid_speelduur("120 min"))
        self.assertTrue(fh.is_valid_speelduur("90 min"))
        self.assertTrue(fh.is_valid_speelduur("9 min"))

        # Invalid values
        self.assertFalse(fh.is_valid_speelduur("90 mix"))
        self.assertFalse(fh.is_valid_speelduur("9x min"))
        self.assertFalse(fh.is_valid_speelduur("x90 min"))
        self.assertFalse(fh.is_valid_speelduur("9O min"))
        self.assertFalse(fh.is_valid_speelduur(""))
        self.assertFalse(fh.is_valid_speelduur(None))

    def test_is_valid_date_string(self):
        # Valid
        self.assertTrue(fh.is_valid_date_string("2020-06-06"))

        # Invalid
        self.assertFalse(fh.is_valid_date_string("2020-0x-06"))
        self.assertFalse(fh.is_valid_date_string("x2020-06-06"))
        self.assertFalse(fh.is_valid_date_string("2020-0x-06x"))
        self.assertFalse(fh.is_valid_date_string(""))
        self.assertFalse(fh.is_valid_date_string(None))

    def test_to_slug(self):

        # standard
        self.assertEqual(fh.to_slug("My own movie"), "my-own-movie")

        # comma
        self.assertEqual(fh.to_slug("My, own movie"), "my-own-movie")
        self.assertEqual(fh.to_slug("Pinocchio (NL)"), "pinocchio-nl")
        self.assertEqual(fh.to_slug("Pinocchio Q&A"), "pinocchio-q-and-a")
        self.assertEqual(fh.to_slug("15:00"), "15-00")
        self.assertEqual(fh.to_slug("Les plus belles années d'une vie"), "les-plus-belles-annees-d-une-vie")
        self.assertEqual(fh.to_slug("Gli anni più belli"), "gli-anni-piu-belli")
        self.assertEqual(fh.to_slug("this/ and that\\"), "this-and-that-")


    def test_create_date_time(self):

        # Valid situation
        result = fh.create_date_time(date_string="2020-06-07", time_string="13:00:00")
        expected = datetime(year=2020, month=6, day=7, hour=13, minute=00, second=00)
        self.assertEqual(result, expected)

        # invalid time-string
        with self.assertRaises(ValueError):
            result = fh.create_date_time(date_string="2020-06-07", time_string="13:00")

        # invalid time-string
        with self.assertRaises(ValueError):
            result = fh.create_date_time(date_string="2020-06-07", time_string="1300")

        # None values
        with self.assertRaises(ValueError):
            result = fh.create_date_time(date_string=None, time_string="13;00")
        with self.assertRaises(ValueError):
            result = fh.create_date_time(date_string="2020-06-07", time_string=None)


    def test_get_date_str(self):

        # valid
        date_string = "2020-07-20"
        time_string = "23:30:00"
        date_time = fh.create_date_time(date_string, time_string)
        result = fh.get_date_str(date_time)
        self.assertEqual(result, date_string)

        # invalid: None
        with self.assertRaises(ValueError):
            fh.get_date_str(None)

    def test_get_time_str(self):

        # valid
        date_string = "2020-07-20"
        time_string = "23:30:00"
        date_time = fh.create_date_time(date_string, time_string)
        result = fh.get_time_str(date_time)
        self.assertEqual(result, time_string)

        # invalid: None
        with self.assertRaises(ValueError):
            fh.get_time_str(None)


    def test_add_minutes_to_datetime(self):

        # valid: adding 0 minutes must return same datetime
        start_date_string = "2020-07-20"
        start_time_string = "23:30:00"
        start_date_time = fh.create_date_time(start_date_string, start_time_string)
        self.assertEqual(fh.add_minutes_to_datetime(start_date_time, 0), start_date_time)

        # valid: add couple of minutes: 15
        end_date_time = fh.add_minutes_to_datetime(start_date_time, 15)
        end_date_string = fh.get_date_str(end_date_time)
        end_time_string = fh.get_time_str(end_date_time)
        self.assertEqual(end_date_string, "2020-07-20")
        self.assertEqual(end_time_string, "23:45:00")

        # valid: add value passing midnight
        end_date_time = fh.add_minutes_to_datetime(start_date_time, 30)
        end_date_string = fh.get_date_str(end_date_time)
        end_time_string = fh.get_time_str(end_date_time)
        self.assertEqual(end_date_string, "2020-07-21")
        self.assertEqual(end_time_string, "00:00:00")

        # invalid: None values
        with self.assertRaises(ValueError):
            fh.add_minutes_to_datetime(None, 30)
        with self.assertRaises(ValueError):
            fh.add_minutes_to_datetime(start_date_time, None)

    def test_get_minutes(self):

        # valid
        self.assertEqual(fh.get_minutes(speelduur="9 min"), 9)
        self.assertEqual(fh.get_minutes(speelduur="90 min"), 90)
        self.assertEqual(fh.get_minutes(speelduur="190 min"), 190)

        # invalid
        with self.assertRaises(ValueError):
            fh.get_minutes(speelduur="x min")
        with self.assertRaises(ValueError):
            fh.get_minutes(speelduur="9 mi")
        with self.assertRaises(ValueError):
            fh.get_minutes(speelduur="99")
        with self.assertRaises(ValueError):
            fh.get_minutes(speelduur=None)
        with self.assertRaises(ValueError):
            fh.get_minutes(speelduur="")


    def test_create_event_row_full(self):
        row: List[str] = ["2020-06-29",
                          "20:30",
                          "Ema, the movie",
                          "Spaans",
                          "drama, muziek",
                          "102 min",
                          "Bas, Eelco",
                          "Ema, de nieuwe film van regisseur Pablo Larraín (Jackie).",
                          "Ema is een explosief, stijlvol en gewaagd portret van een danseres.",
                          "https://tickets.de-fabriek.nl/fabriek/nl/flow_configs/webshop/steps/start/show/428247",
                          "https://www.de-fabriek.nl/films/290-ema.html"]
        # event_start_date,event_start_time,event_end_date,event_end_time,event_name,event_slug,post_content,location,category
        expected = ["2020-06-29","20:30:00","2020-06-29","22:22:00",
                    '"Ema, the movie"',
                    "\"Ema, de nieuwe film van regisseur Pablo Larraín (Jackie).\"",
                    "\"<strong>Ema, de nieuwe film van regisseur Pablo Larraín (Jackie).</strong><br><br>"
                    "Ema is een explosief, stijlvol en gewaagd portret van een danseres.<br>"
                    "<br>"
                    "<strong>Gesproken taal: </strong>Spaans<br>"
                    "<strong>Genre: </strong>drama, muziek<br>"
                    "<strong>Speelduur: </strong>102 min<br>"
                    "<br>"
                    "<a href=\'https://www.de-fabriek.nl/films/290-ema.html\'>"
                    "https://www.de-fabriek.nl/films/290-ema.html</a>\"",
                    "filmtheater-de-fabriek-2",
                    "film"]
        result = fh.create_event_row(row)
        self.assertEqual(result, expected)

    def test_create_event_row_full_no_date(self):
        row: List[str] = ["",
                          "20:30",
                          "Ema, the movie",
                          "Spaans",
                          "drama, muziek",
                          "102 min",
                          "Bas, Eelco",
                          "Ema, de nieuwe film van regisseur Pablo Larraín (Jackie).",
                          "Ema is een explosief, stijlvol en gewaagd portret van een danseres.",
                          "https://tickets.de-fabriek.nl/fabriek/nl/flow_configs/webshop/steps/start/show/428247",
                          "https://www.de-fabriek.nl/films/290-ema.html"]
        with self.assertRaises(ValueError):
            fh.create_event_row(row)

    def test_create_event_manager_file(self):
        currentDirectory = os.getcwd()
        input_file = open(f"../../../test/fabriek_sorted_test_01_OK.csv")
        output_file = open(f"../../../output/fabriek_event_manager_test_01_OK.csv", mode="w")
        fh.create_event_manager_file(input_file=input_file, output_file=output_file)

    def test_create_event_manager_file_invalid_no_date(self):
        input_file = open(f"../../../test/fabriek_sorted_test_02_2nd_movie_no_date.csv")
        output_file = open(f"../../../output/fabriek_event_manager_test_02_2nd_movie_no_date.csv", mode="w")
        fh.create_event_manager_file(input_file=input_file, output_file=output_file)


    def test_encoding_issues_step_1_sort_file_with(self):
        input_file = open(f"../../../test/fabriek_2020-08-03_134658_01_encoding.csv", encoding="utf-8")
        output_file = open(f"../../../output/fabriek_2020-08-03_134658_01_encoding_sorted.csv", mode="w")
        fh.create_sorted_file(input_file=input_file, output_file=output_file)

    def test_encoding_issues_step_1_create_event_manager_file(self):
        input_file = open(f"../../../test/fabriek_2020-08-03_134658_02_encoding_sorted.csv", encoding="utf-8")
        output_file = open(f"../../../output/fabriek_2020-08-03_134658_03_encoding_event_manager.csv", mode="w")
        fh.create_sorted_file(input_file=input_file, output_file=output_file)

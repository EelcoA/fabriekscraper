from unittest import TestCase

from fabriek.file_handling import correct_path_for_scrapy_on_windows

class Test(TestCase):

    def test_correct_path_for_scrapy_on_window_LINUX(self):
        path = "/home/user/test/myfile.csv"
        corrected_path = correct_path_for_scrapy_on_windows(path)
        self.assertEqual(path, corrected_path)

    def test_correct_path_for_scrapy_on_window_WIN_C_DRIVE(self):
        path = "c:/home/user/test/myfile.csv"
        corrected_path = correct_path_for_scrapy_on_windows(path)
        expected_corrected_path = "file:///c:/home/user/test/myfile.csv"
        self.assertEqual(expected_corrected_path, corrected_path)

    def test_correct_path_for_scrapy_on_window_WIN_D_DRIVE(self):
        path = "d:/home/user/test/myfile.csv"
        corrected_path = correct_path_for_scrapy_on_windows(path)
        expected_corrected_path = "file:///d:/home/user/test/myfile.csv"
        self.assertEqual(expected_corrected_path, corrected_path)

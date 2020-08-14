import os
import unittest

from fabriek.spiders import fabriek_helper as fh, fabriek_spider
from definitions import TEST_RESPONSES
from tests.src import test_webpages_helper as helper

class FabriekSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = fabriek_spider.FabriekSpider()

    # def _test_item_results(self, results, expected_length):
    #     count = 0
    #     permalinks = set()
    #     for item in results:
    #         self.assertIsNotNone(item['content'])
    #         self.assertIsNotNone(item['title'])
    #     self.assertEqual(count, expected_length)

    def test_parse(self):
        print('in test_parse ')
        response = helper.fake_response_from_file(os.path.join(TEST_RESPONSES, 'TheSouvenir.html'))
        result = fh.parse_movie(response=response,
                                title="The Souvenir",
                                day="2020-08-01",
                                time="10:10",
                                ticket_url="https://www.de-fabriek.nl/films/404-the+souvenir.html/ticket",
                                movie_url="https://www.de-fabriek.nl/films/404-the+souvenir.html")
        for i in result:
            print(i)

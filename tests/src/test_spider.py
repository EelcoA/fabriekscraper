import os
import unittest
from pprint import pprint

import tests.src.util
from fabriek.spiders import fabriek_spider
from definitions import TEST_RESPONSES


class SpiderTest(unittest.TestCase):

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
        response = tests.src.util.fake_response_from_file(os.path.join(TEST_RESPONSES, 'TheSouvenir.html'))
        result = self.spider.parse_movie(response=response,
                                         title="The Souvenir",
                                         day="2020-08-01",
                                         time="10:10",
                                         ticket_url="https://www.de-fabriek.nl/films/404-the+souvenir.html/ticket",
                                         movie_url="https://www.de-fabriek.nl/films/404-the+souvenir.html")

        for i in result:
            pprint(i)

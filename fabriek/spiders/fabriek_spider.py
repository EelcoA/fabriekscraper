# -*- coding: utf-8 -*-
from typing import List
import scrapy
from scrapy.spiders import CrawlSpider
from fabriek.spiders import fabriek_helper as fh


class FabriekSpider(CrawlSpider):
    name = 'fabriek'
    allowed_domains = ['www.de-fabriek.nl']
    start_urls = ['https://www.de-fabriek.nl']
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
    }

    def parse(self, response):
        day_urls = response.xpath("//a[@class='day-selector__day']/@href").getall()
        for day_url in day_urls:
            day = day_url[-10:]  # yyyy-mm-dd
            complete_url = self.start_urls[0] + day_url
            yield scrapy.Request(url=complete_url, callback=self.parse_day,
                                 priority=10,
                                 cb_kwargs=dict(day=day))

    def parse_day(self, response, day: str):
        self.logger.debug("PARSE_DAY: " + day)
        #
        # for movie_urls and movie_titles I added [not(@class)] because with 'specials' there were two links and titles
        # found, but only 1 time and ticket, causing the index to go out of bound.
        #
        # to prevent this type of errors unnoticed, I've added a check on the size of all 4 Lists
        #
        movie_urls: List[str] = response.xpath(
            "//div[@class='main-agenda-movie-info']/h4/a[not(@class)]/@href").getall()
        movie_times: List[str] = response.xpath("//div[@class='main-agenda-movie-time']/a/text()").getall()
        movie_titles: List[str] = response.xpath(
            "//div[@class='main-agenda-movie-info']/h4/a[not(@class)]/text()").getall()
        movie_tickets: List[str] = response.xpath("//a[@class='button ticket-button']/@href").getall()
        if len(movie_urls) == len(movie_times) == len(movie_titles) == len(movie_tickets):
            pass
        else:
            self.logger.error(
                "Het verwerken van de gegevens van dag " + day + "is niet goed gegaan. Check de films van die dag!")
        i: int = 0

        for movie_title in movie_titles:
            yield scrapy.Request(url=self.start_urls[0] + movie_urls[i], callback=fh.parse_movie,
                                 priority=10,
                                 dont_filter=True,
                                 cb_kwargs=dict(title=movie_title,
                                                day=day,
                                                time=movie_times[i],
                                                ticket_url=movie_tickets[i],
                                                movie_url=self.start_urls[0] + movie_urls[i]))
            i += 1



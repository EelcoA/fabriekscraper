# -*- coding: utf-8 -*-
from typing import List
import scrapy
from scrapy.spiders import CrawlSpider


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
                "Het verwerken van de gegevens van dag " + day + " is niet goed gegaan. Check de films van die dag!")
        i: int = 0

        for movie_title in movie_titles:
            yield scrapy.Request(url=self.start_urls[0] + movie_urls[i], callback=self.parse_movie,
                                 priority=10,
                                 dont_filter=True,
                                 cb_kwargs=dict(title=movie_title,
                                                day=day,
                                                time=movie_times[i],
                                                ticket_url=movie_tickets[i],
                                                movie_url=self.start_urls[0] + movie_urls[i]))
            i += 1

    def parse_movie(self, response, title, day, time, ticket_url, movie_url):
        title: str = response.xpath("//div[@class='hero-slide-content']/h1/text()").get()
        language: str = get_text_from_movie(response, "Gesproken taal:")
        genres: str = get_text_from_movie(response, "Genre:")
        playing_time: str = get_text_from_movie(response, "Speelduur:")
        cast: str = get_text_from_movie(response, "Cast:")
        synopsis: str = response.xpath("//p[@class='film__synopsis__intro']/strong/text()").get()
        content_detail_list: List[str] = response.xpath("//div[@class='film__content__details__left']/p").getall()
        content_detail = "".join(content_detail_list)

        yield {'datum': day,
               'tijd': time,
               'titel': title,
               'taal': language,
               'genre': genres,
               'speelduur': playing_time,
               'cast': cast,
               'synopsis': synopsis,
               'beschrijving': content_detail,
               'ticket-url': ticket_url,
               'film-url': movie_url
               }


def get_text_from_movie(response, param):
    text = response.xpath("//div[@class='film__content__meta']/p/strong[text()='" + param + "']/../text()").get()
    if text is not None:
        text = text.strip()
    return text

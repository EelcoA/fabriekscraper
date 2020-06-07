# -*- coding: utf-8 -*-
import os
from typing import Dict, List
import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def get_text_from_movie(response, param):
    text = response.xpath("//div[@class='film__content__meta']/p/strong[text()='" + param + "']/../text()").get()
    if text is not None:
        text = text.strip()
    return text


class FabriekSpider(CrawlSpider):
    name = 'fabriek'
    allowed_domains = ['www.de-fabriek.nl']
    start_urls = ['https://www.de-fabriek.nl']

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
        movie_urls: List[str] = response.xpath("//div[@class='main-agenda-movie-info']/h4/a/@href").getall()
        movie_times: List[str] = response.xpath("//div[@class='main-agenda-movie-time']/a/text()").getall()
        movie_titles: List[str] = response.xpath("//div[@class='main-agenda-movie-info']/h4/a/text()").getall()
        movie_tickets: List[str] = response.xpath("//a[@class='button ticket-button']/@href").getall()
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
        self.logger.debug("PARSE_MOVIE: " + title)
        title: str = response.xpath("//div[@class='hero-slide-content']/h1/text()").get()
        language: str = get_text_from_movie(response, "Gesproken taal:")
        genres: str = get_text_from_movie(response, "Genre:")
        playing_time: str = get_text_from_movie(response, "Speelduur:")
        cast: str = get_text_from_movie(response, "Cast:")
        synopsis: str = response.xpath("//p[@class='film__synopsis__intro']/strong/text()").get()
        content_detail1 = response.xpath("//div[@class='film__content__details__left']/p[1]/text()").get()
        content_detail2 = response.xpath("//div[@class='film__content__details__left']/p[2]/text()").get()
        content_detail3 = response.xpath("//div[@class='film__content__details__left']/p[3]/text()").get()
        content_detail = ""
        if content_detail1 is not None:
            content_detail += content_detail1
        if content_detail2 is not None:
            content_detail += content_detail2
        if content_detail3 is not None:
            content_detail += content_detail3

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




def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

output_csv_file: str = "../../output/fabriek.csv"
output_csv_file_sorted: str = "../../output/fabriek-sorted.csv"

delete_file(output_csv_file)
delete_file(output_csv_file_sorted)


process = CrawlerProcess(settings={
    "FEEDS": {
        output_csv_file: {"format": "csv"},
    }
})

process.crawl(FabriekSpider)
process.start()  # the script will block here until the crawling is finished

# open and read the file

with open(output_csv_file) as csv_file:
    header_row: List[str]
    movie_list: List[List[str]] = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            header_row = row
            line_count += 1
        else:
            movie_list.append(row)

movie_list.sort()
output_file = open(output_csv_file_sorted, mode="w")
output_file.write(",".join(header_row) + "\n")
for row in movie_list:
    output_file.write(",".join(row) + "\n")
output_file.close()
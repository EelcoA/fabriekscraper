# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess

from fabriek import file_handling
from fabriek.csv_convert import sort, event_manager
from fabriek.spiders.fabriek_spider import FabriekSpider


def run():
    filename_prefix = file_handling.create_filename_prefix_with_date_and_time()

    crawl_data_fileName = filename_prefix + "_01.csv"
    crawl_fabriek_website(output_filename=crawl_data_fileName)

    sorted_data_fileName = filename_prefix + "_02_sorted.csv"
    sort_crawl_data(input_filename=crawl_data_fileName, output_filename=sorted_data_fileName)

    event_data_filename = filename_prefix + "_03_event_manager.csv"
    create_event_data_file(sorted_data_fileName, event_data_filename)


def crawl_fabriek_website(output_filename):
    output_filepath = file_handling.create_filepath_for_file_in_output_dir(output_filename)
    crawl_fabriek_website_into_file(output_filepath=output_filepath)
    print("\nBestand met film data            : " + output_filepath)


def crawl_fabriek_website_into_file(output_filepath: str):
    process = CrawlerProcess(settings={
        "FEEDS": {
            output_filepath: {"format": "csv"},
        }
    })
    process.crawl(FabriekSpider)
    process.start()  # the script will block here until the crawling is finished


def sort_crawl_data(input_filename, output_filename):
    input_file_wrapper = file_handling.open_file_for_input(input_filename)
    output_file_wrapper = file_handling.open_file_for_output(output_filename)
    sort.sort_crawl_output_into_new_file(input_file_wrapper, output_file_wrapper)


def create_event_data_file(input_filename, output_filename):
    input_file_wrapper = file_handling.open_file_for_input(input_filename)
    output_file_wrapper = file_handling.open_file_for_output(output_filename)
    event_manager.create_event_manager_file(input_file_wrapper, output_file_wrapper)

# -*- coding: utf-8 -*-

try:
    import scrapy.crawler
except ImportError as ie:
    print('Scrapy kan niet geladen worden, controleer de installatie van Scrapy')
    exit()

from fabriek import file_handling
from fabriek.csv_convert import sort, event, orkaan
try:
    from fabriek.spiders.fabriek_spider import FabriekSpider
except ImportError as ie:
    print('FabriekSpider kan niet geladen worden, controleer de installatie van Scrapy')
    exit()


def run():
    filename_prefix = file_handling.create_filename_prefix_with_date_and_time()

    crawl_data_filename = filename_prefix + "_01.csv"
    crawl_fabriek_website(output_filename=crawl_data_filename)

    sorted_data_fileName = filename_prefix + "_02_sorted.csv"
    sort_crawl_data(input_filename=crawl_data_filename, output_filename=sorted_data_fileName)

    # event_data_filename = filename_prefix + "_03_event_manager.csv"
    # create_event_data_file(sorted_data_fileName, event_data_filename)
    
    orkaan_agenda_filename = filename_prefix + "_04_orkaan_agenda.txt"
    create_orkaan_agenda_file(sorted_data_fileName, orkaan_agenda_filename)


def crawl_fabriek_website(output_filename):
    output_filepath = file_handling.create_filepath_for_file_in_output_dir(output_filename)
    corrected_output_filepath = file_handling.correct_path_for_scrapy_on_windows(output_filepath)
    crawl_fabriek_website_into_file(output_filepath=corrected_output_filepath)
    print("Bestand met film data            : " + output_filepath)


def crawl_fabriek_website_into_file(output_filepath: str):
    process = scrapy.crawler.CrawlerProcess(settings={
        "FEEDS": {
            output_filepath: {"format": "csv"},
        }
    })
    process.crawl(FabriekSpider)
    process.start()  # the script will block here until the crawling is finished


def sort_crawl_data(input_filename, output_filename):
    input_file_wrapper = file_handling.open_file_for_input(input_filename)
    output_file_wrapper = file_handling.open_file_for_output(output_filename)
    sort.sort_crawl_data_into_new_file(input_file_wrapper, output_file_wrapper)

    print("Bestand met gesorteerde film data: " + output_file_wrapper.name)


def create_event_data_file(input_filename, output_filename):
    input_file_wrapper = file_handling.open_file_for_input(input_filename)
    output_file_wrapper = file_handling.open_file_for_output(output_filename)
    event.create_event_manager_file(input_file_wrapper, output_file_wrapper)

    print("Bestand met eventmanager data    : " + output_file_wrapper.name)


def create_orkaan_agenda_file(input_filename, output_filename):
    input_file_wrapper = file_handling.open_file_for_input(input_filename)
    output_file_wrapper = file_handling.open_file_for_output(output_filename)
    orkaan.create_orkaan_agenda_file(input_file_wrapper, output_file_wrapper)

    print("Bestand met agenda voor De Orkaan: " + output_file_wrapper.name)


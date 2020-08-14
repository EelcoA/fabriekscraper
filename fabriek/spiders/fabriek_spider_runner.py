# -*- coding: utf-8 -*-
import io
import datetime as dt
from scrapy.crawler import CrawlerProcess
from fabriek.spiders import fabriek_helper as fh
from fabriek.spiders.fabriek_spider import FabriekSpider


def create_file_fame_prefix_with_date_and_time() -> str:
    datetime = dt.datetime.now()
    return f"fabriek_{datetime:%Y-%m-%d_%H%M%S}"


def crawl_fabriek_website(outputFilename):
    outputFilePath = fh.create_filepath_for_file_in_output_dir(outputFilename)
    crawl_fabriek_website_into_file(outputFilePath=outputFilePath)
    print("\nBestand met film data            : " + outputFilePath)


def crawl_fabriek_website_into_file(outputFilePath: str):
    process = CrawlerProcess(settings={
        "FEEDS": {
            outputFilePath: {"format": "csv"},
        }
    })
    process.crawl(FabriekSpider)
    process.start()  # the script will block here until the crawling is finished


def sort_crawl_data(inputFileName, outputFileName):
    inputFileWrapper = fh.open_file_for_input(inputFileName)
    outputFileWrapper = fh.open_file_for_output(outputFileName)
    fh.sort_crawl_output_into_new_file(inputFileWrapper, outputFileWrapper)


def create_event_data_file(inputFileName, outputFileName):
    inputFileWrapper = fh.open_file_for_input(inputFileName)
    outputFileWrapper = fh.open_file_for_output(outputFileName)
    fh.create_event_manager_file(inputFileWrapper, outputFileWrapper)


def run():
    fileNamePrefix = create_file_fame_prefix_with_date_and_time()

    crawlDataFileName = fileNamePrefix + "_01.csv"
    crawl_fabriek_website(outputFilename=crawlDataFileName)

    sortedDataFileName = fileNamePrefix + "_02_sorted.csv"
    sort_crawl_data(inputFileName=crawlDataFileName, outputFileName=sortedDataFileName)

    eventDataFileName = fileNamePrefix + "_03_event_manager.csv"
    create_event_data_file(sortedDataFileName, eventDataFileName)

# -*- coding: utf-8 -*-
import io
import datetime as dt
from scrapy.crawler import CrawlerProcess
from fabriek.spiders import fabriek_helper as fh
from fabriek.spiders.fabriek_spider import FabriekSpider


def createFileNamePrefixWithDateAndTime() -> str:
    datetime = dt.datetime.now()
    return f"fabriek_{datetime:%Y-%m-%d_%H%M%S}"


def crawlFabriekWebsite(outputFilename):
    outputFilePath = fh.createFilePathForFileInOutputDir(outputFilename)
    crawlFabriekWebsiteIntoFile(outputFilePath=outputFilePath)
    print("\nBestand met film data            : " + outputFilePath)


def crawlFabriekWebsiteIntoFile(outputFilePath: str):
    process = CrawlerProcess(settings={
        "FEEDS": {
            outputFilePath: {"format": "csv"},
        }
    })
    process.crawl(FabriekSpider)
    process.start()  # the script will block here until the crawling is finished


def sortCrawlData(inputFileName, outputFileName):
    inputFileWrapper = fh.openFileForInput(inputFileName)
    outputFileWrapper = fh.openFileForOutput(outputFileName)
    fh.sortCrawlOutputIntoNewFile(inputFileWrapper, outputFileWrapper)


def createEventDataFile(inputFileName, outputFileName):
    inputFileWrapper = fh.openFileForInput(inputFileName)
    outputFileWrapper = fh.openFileForOutput(outputFileName)
    fh.create_event_manager_file(inputFileWrapper, outputFileWrapper)


def run():
    fileNamePrefix = createFileNamePrefixWithDateAndTime()

    crawlDataFileName = fileNamePrefix + "_01.csv"
    crawlFabriekWebsite(outputFilename=crawlDataFileName)

    sortedDataFileName = fileNamePrefix + "_02_sorted.csv"
    sortCrawlData(inputFileName=crawlDataFileName, outputFileName=sortedDataFileName)

    eventDataFileName = fileNamePrefix + "_03_event_manager.csv"
    createEventDataFile(sortedDataFileName, eventDataFileName)

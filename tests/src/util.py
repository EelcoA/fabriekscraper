import io
import os
from typing import List

from scrapy import Request
from scrapy.http import Response, HtmlResponse

import definitions
from definitions import ROOT_DIR


def open_test_file_for_input(inputFileName):
    inputFileNamePath = os.path.join(ROOT_DIR, "tests", "resources", inputFileName)
    return open(inputFileNamePath, encoding="utf-8")


def open_test_inputfile_for_output(outputFileName) -> object:
    outputFileNamePath = os.path.join(ROOT_DIR, "tests", "resources", outputFileName)
    return open(outputFileNamePath, mode="w", encoding="utf-8")


def open_test_file_for_output(outputFileName):
    outputFileNamePath = os.path.join(ROOT_DIR, "tests", "output", outputFileName)
    return open(outputFileNamePath, mode="w", encoding="utf-8")


def create_in_memory_test_output_file():
    """
    This creates an in memory file. There is one conflicting difference with a real file:
    - closing an in memory file causes the data to be removed.
    By using a flag in the name I work around this issue. The program tests on this flag,
    then it doesn't close it.
    """
    file = io.StringIO()
    file.name = definitions.FLAG_TO_SKIP_CLOSING_OF_IN_MEMORY_TEST_FILE
    return file


class TestData:
    line_feed = '\n'
    rows: List[str] = []

    def __init__(self, *rows):
        for row in rows:
            self.rows.append(row)


def create_test_file(file_name: str, test_file: TestData):
    """
    This creates a real file. I preferred an in memory file, but the behaviour
    was too different from a real file, causing too many errors.
    """
    temp_file = open_test_inputfile_for_output(file_name)
    for line in test_file.rows:
        temp_file.write(line + test_file.line_feed)
    temp_file.close()

    return open_test_file_for_input(file_name)


def get_rows_from_test_output(test_output_file: io.StringIO) -> List[str]:
    output = test_output_file.getvalue()
    lines = output.split("\r\n")
    return lines


def fake_response_from_file(file_name, url=None) -> Response:
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.de-fabriek.nl'

    request = Request(url=url)
    if not file_name[0] == '/':
        file_path = os.path.join(definitions.ROOT_DIR, file_name)
    else:
        file_path = file_name

    open_file = open(file_path)
    file_content = open_file.read()
    open_file.close()

    response = HtmlResponse(url=url,
                            request=request,
                            body=file_content,
                            encoding="utf-8")


    return response
import os
import definitions
from scrapy.http import Response, Request, HtmlResponse, TextResponse


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

    file_content = open(file_path, 'r').read()

    response = HtmlResponse(url=url,
                            request=request,
                            body=file_content,
                            encoding="utf-8")
    return response

import csv
from typing import List, IO

import definitions


def sort_crawl_data_into_new_file(input_file: IO, output_file: IO):
    headerAndMovies = get_header_and_movies_from(input_file)
    headerAndMovies.sort_movies()
    write_sorted_output(headerAndMovies, output_file)


class HeaderAndMovies():
    header_row: List[str]
    movie_list: List[List[str]] = []

    def __init__(self, header_row: List[str], movie_list: List[List[str]]):
        self.header_row = header_row
        self.movie_list = movie_list

    def sort_movies(self):
        self.movie_list.sort()


def get_header_and_movies_from(input_file) -> HeaderAndMovies:
    movie_list: List[List[str]] = []
    with input_file as csv_file:
        csv_reader = csv.reader(csv_file,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL,
                                skipinitialspace=True)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header_row = row
            else:
                movie_list.append(row)
            line_count += 1

    return HeaderAndMovies(header_row, movie_list)


def write_sorted_output(headerAndMovies: HeaderAndMovies, output_file):
    writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headerAndMovies.header_row)
    for row in headerAndMovies.movie_list:
        writer.writerow(row)

    if output_file.name != definitions.FLAG_TO_SKIP_CLOSING_OF_IN_MEMORY_TEST_FILE:
        output_file.close()


import csv
from typing import List


def sort_crawl_output_into_new_file(input_file, output_file):
    header_row: List[str]
    movie_list: List[List[str]] = []

    with input_file as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                header_row = row
            else:
                movie_list.append(row)
            line_count += 1

    movie_list.sort()

    writer = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(header_row)
    for row in movie_list:
        writer.writerow(row)
    output_file.close()

    print("\nBestand met gesorteerde film data: " + output_file.name)

    return None
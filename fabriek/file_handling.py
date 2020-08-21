import datetime as dt
import os

from definitions import OUTPUT_DIR


def create_filename_prefix_with_date_and_time() -> str:
    datetime = dt.datetime.now()
    return f"fabriek_{datetime:%Y-%m-%d_%H%M%S}"


def create_filepath_for_file_in_output_dir(fileName: str) -> str:
    file_path: str = os.path.join(OUTPUT_DIR, fileName)
    return file_path


def correct_path_for_scrapy_on_windows(file_path):
    if file_path.startswith(":", 1):
        return "file:///" + file_path
    else:
        return file_path


def open_file_for_input(inputFileName):
    inputFilePath = create_filepath_for_file_in_output_dir(inputFileName)
    return open(inputFilePath, encoding="utf-8")


def open_file_for_output(outputFileName):
    outputFileNamePath = create_filepath_for_file_in_output_dir(outputFileName)
    return open(outputFileNamePath, mode="w", newline='', encoding="utf-8")

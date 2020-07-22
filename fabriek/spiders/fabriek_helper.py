import csv
import io
import re
import time
import unicodedata
import datetime as dt
from typing import List


def to_strong(text: str):
    """
    Returns the text surrounded with <strong> and </strong> elements
    :param text:
    :return: String with text, or None when none was given or empty string when no
             text was found in input (empty string or just spaces)
    """
    if text is None:
        return None
    if text.strip() == "":
        return ""
    return "<strong>" + text + "</strong>"


def is_pattern_matching(pattern_str: str, value: str) -> bool:
    """
    Helps to get a boolean out of the pattern matching
    :param pattern_str: regex pattern string
    :param value: value to be tested
    :return: true when there was a match, false if None
    """
    if value is None:
        return False
    if value.strip() is "":
        return False

    pattern = re.compile(pattern_str)
    match = pattern.match(value)
    if match is None:
        result = False
    else:
        result = True
    return result


def is_valid_begintijd(time: str) -> bool:
    """
    Check if tijd contains hh:mm
    :param tijd:
    :return: True or False
    """
    result = is_pattern_matching("^[0-9][0-9]:[0-9][0-9]$", time)
    return result


def is_valid_speelduur(speelduur: str) -> bool:
    """
    Checks if speelduur contains "<int of 1,2,3 pos> min"
    :param speelduur:
    :return: True or False
    """
    result = is_pattern_matching("^[0-9]* min$", speelduur)
    return result


def is_valid_date_string(datum: str) -> bool:
    """
    Test if string contains a valid date value in format YYYY-MM-DD
    :param datum:
    :return: True or False
    """
    result = is_pattern_matching("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", datum)
    return result

def is_valid_time_string(time: str) -> bool:
    """
    Check if tijd contains hh:mm:ss
    :param tijd:
    :return: True or False
    """
    result = is_pattern_matching("^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$", time)
    return result

def to_slug(titel: str):
    """
    Converst a string (with for example film title names in French, to a url ready version
    :param titel:
    :return:
    """
    result = titel \
        .replace(" ", "-") \
        .replace("--", "-") \
        .replace("!", "") \
        .replace("\"", "-") \
        .replace("#", "") \
        .replace("$", "dollar") \
        .replace("%", "perc") \
        .replace("&", "-and-") \
        .replace("'", "-") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("*", "-") \
        .replace("+", "-") \
        .replace(",", "") \
        .replace(":", "-") \
        .replace(".", "-") \
        .replace("/", "-") \
        .replace("\\", "-") \
        .replace(";", "-") \
        .replace("<", "") \
        .replace(">", "") \
        .replace("?", "") \
        .replace("@", "AT-") \
        .replace("[", "") \
        .replace("]", "") \
        .replace("^", "") \
        .replace("{", "") \
        .replace("}", "") \
        .replace("|", "") \
        .replace("~", "") \
        .replace("---", "-") \
        .replace("--", "-") \
        .lower()
    result = unicodedata.normalize('NFD', result).encode('ascii', 'ignore').decode("utf-8")
    return result


def create_date_time(date_string: str, time_string: str) -> dt.datetime:
    """
    Create a datetime from a date-string  and a time-string
    :param date_string: format YYYY-mm-DD
    :param time_string: format HH:MM:SS
    :return: valid datetime object
    :raises ValueError when date_string or time_string don't contain the right values
    """
    if not is_valid_date_string(date_string):
        raise ValueError("\"date_string has no correct value (yyyy:mm:dd): " +
                         ("None" if date_string is None else date_string) + "\"")
    if not is_valid_time_string(time_string):
        raise ValueError("\"time_string has no correct value (hh:mm:ss): " +
                         ("None" if time_string is None else time_string) + "\"")

    jjjjmmdd = date_string.split("-")
    jjjj = int(jjjjmmdd[0])
    MM = int(jjjjmmdd[1])
    dd = int(jjjjmmdd[2])

    hhmmss = time_string.split(":")
    hh = int(hhmmss[0])
    mm = int(hhmmss[1])
    ss = int(hhmmss[2])

    return dt.datetime(jjjj, MM, dd, hh, mm, ss)


def get_date_str(date_time: dt.datetime) -> str:
    """
    Get a string with the date in YYYY-MM-DD format from the given datetime
    :param date_time:
    :return: YYYY-MM-DD
    :raises ValueError when input is None
    """
    if date_time is None:
        raise ValueError("Given date_time should have value, but is None")
    return date_time.strftime("%Y-%m-%d")


def get_time_str(date_time: dt.datetime) -> str:
    """
    Get a string with the time in HH:MM:SS format from the given datetime
    :param date_time:
    :return: HH-MM-SS
    :raises ValueError when input is None
    """
    if date_time is None:
        raise ValueError("Given date_time should have value, but is None")
    return date_time.strftime("%H:%M:%S")


def add_minutes_to_datetime(start_date_time: dt.datetime, minutes: int) -> dt.datetime:
    """
    Add minutes to the datetime and return the resulting datetime
    :param start_date_time:
    :param minutes:
    :return: start_date_time + minutes
    :raises ValueError when (one of the) input fields are None
    """
    if start_date_time is None:
        raise ValueError("start_date_time has no value")
    if minutes is None:
        raise ValueError("minutes has no value")

    timedelta = dt.timedelta(minutes=minutes)
    return start_date_time + timedelta


def get_minutes(speelduur: str) -> int:
    """
    Gets the minutes out of the field speelduur
    :param speelduur: String filled with "9[9][9] min"
    :return: minutes playing time
    :raise ValueError when speelduur is None or has no valid value
    """
    if not is_valid_speelduur(speelduur):
        raise ValueError("\"Speelduur value not valid, must be '99[9] min', but is: " +
                         ( "leeg" if speelduur is None else speelduur ) + "\"")

    # get speelduur, make sure it is digits
    speelduur_list = speelduur.split(" ")
    min_speelduur_str: str = speelduur_list[0]
    min_speelduur = int(min_speelduur_str)
    return min_speelduur


def create_event_row(row: List[str]):

    # get all fields out of the List
    datum = row[0]
    tijd = row[1]
    titel = row[2]
    taal = row[3]
    genre = row[4]
    speelduur = row[5]
    cast = row[6]
    synopsis = row[7]
    beschrijving = row[8]
    ticket_url = row[9]
    film_url = row[10]

    if not is_valid_date_string(datum):
        raise ValueError("\"datum bevat geen of geen geldige waarde: " + ("Leeg" if datum is None else datum) + "\"")
    event_start_date = datum

    if not is_valid_begintijd(tijd):
        raise ValueError("\"tijd bevat geen, of geen geldige waarde: " + ( "Leeg" if tijd is None else tijd) + "\"")
    event_start_time = tijd + ":00"

    playtime_minutes = get_minutes(speelduur)
    start_date_time: dt.datetime = create_date_time(event_start_date, event_start_time)
    end_date_time: dt.datetime   = add_minutes_to_datetime(start_date_time, playtime_minutes)

    event_end_date = get_date_str(end_date_time)
    event_end_time = get_time_str(end_date_time)

    event_name = '"' + titel + '"'
    event_slug = to_slug(titel) + "_" + datum + "_" + to_slug(tijd)
    post_content = '"' + \
                   ((to_strong(synopsis) + "<br>" + "<br>") if synopsis != "" else "") + \
                   beschrijving + "<br>" + \
                   "<br>" + \
                   to_strong("Gesproken taal: ") + taal + "<br>" + \
                   to_strong("Genre: ") + genre + "<br>" + \
                   to_strong("Speelduur: ") + speelduur + "<br>" + \
                   "<br>" + \
                   film_url + \
                   '"'
    location = "filmtheater-de-fabriek-2"
    category = "film"

    event_row = [event_start_date, event_start_time, event_end_date, event_end_time,
                 event_name, event_slug, post_content, location, category]

    return event_row


def create_event_manager_file(input_file: io.IOBase, output_file: io.IOBase):
    """

    :param input_file:
    :type output_file: object
    """
    header_row = ["event_start_date", "event_start_time", "event_end_date", "event_end_time", "event_name",
                  "event_slug",
                  "post_content", "location", "category"]
    output_file.write(",".join(header_row) + "\n")

    with input_file as input_file:
        reader = csv.reader(input_file, delimiter=',')
        line_count = 0
        for row in reader:
            if line_count != 0:
                try:
                    event_row = create_event_row(row)
                    output_file.write(",".join(event_row) + "\n")
                except ValueError as e:
                    msg = "Foutieve data van de website, regel " + str(line_count) + ", fout= " + str(e)
                    #
                    print(msg)
                    output_file.write(msg + "\n")
            line_count += 1
    output_file.close()

    return None
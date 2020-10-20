import datetime as dt
import re


def get_minutes(speelduur: str) -> int:
    """
    Gets the minutes out of the field speelduur
    :param speelduur: String filled with "9[9][9] min"
    :return: minutes playing time
    :raise ValueError when speelduur is None or has no valid value
    """
    if not is_valid_speelduur(speelduur):
        raise ValueError("\"Speelduur value not valid, must be '99[9] min', but is: " +
                         ("leeg" if speelduur is None else speelduur) + "\"")

    # get speelduur, make sure it is digits
    speelduur_list = speelduur.split(" ")
    min_speelduur_str: str = speelduur_list[0]
    min_speelduur = int(min_speelduur_str)
    return min_speelduur


def is_valid_speelduur(speelduur: str) -> bool:
    """
    Checks if speelduur contains "<int of 1,2,3 pos> min"
    :param speelduur:
    :return: True or False
    """
    result = is_pattern_matching("^[0-9]* min$", speelduur)
    return result


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


def is_valid_begintijd(time: str) -> bool:
    """
    Check if tijd contains hh:mm
    :param tijd:
    :return: True or False
    """
    result = is_pattern_matching("^[0-9][0-9]:[0-9][0-9]$", time)
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


def is_pattern_matching(pattern_str: str, value: str) -> bool:
    """
    Helps to get a boolean out of the pattern matching
    :param pattern_str: regex pattern string
    :param value: value to be tested
    :return: true when there was a match, false if None
    """
    if value is None:
        return False
    if value.strip() == "":
        return False

    pattern = re.compile(pattern_str)
    match = pattern.match(value)
    if match is None:
        result = False
    else:
        result = True
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


PATTERN_TO_CLEAN_HTML = re.compile(r'<[^>]+>')


def clean_text_from_HTML_and_other_shit(dirty_text: str) -> str:
    clean_text = PATTERN_TO_CLEAN_HTML.sub('', dirty_text)
    return clean_text


def remove_redundant_expert(description: str, excerpt: str) -> str:
    description = description.strip()
    excerpt = excerpt.strip()
    start_pos = description.find(excerpt)
    length_excerpt = len(excerpt)
    if (start_pos == 0):
        description = description[length_excerpt:]
    return description.strip()
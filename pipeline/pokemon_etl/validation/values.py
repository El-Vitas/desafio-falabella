import re
from datetime import datetime

from pokemon_etl.constants.validation import (
    DATE_FORMAT,
    INTEGER_PATTERN,
    MAX_INTEGER_DIGITS,
    TIMESTAMP_FORMAT,
)


def is_integer(text: str) -> bool:
    return re.fullmatch(INTEGER_PATTERN, text.strip()) is not None


def integer_value(text: str) -> int | None:
    digits = text.strip().lstrip("-")
    if not is_integer(text) or len(digits) > MAX_INTEGER_DIGITS:
        return None
    return int(text)


def _parse_datetime(text: str, pattern: str) -> datetime | None:
    try:
        return datetime.strptime(text, pattern)
    except ValueError:
        return None


def parse_date(text: str) -> datetime | None:
    return _parse_datetime(text, DATE_FORMAT)


def parse_timestamp(text: str) -> datetime | None:
    return _parse_datetime(text, TIMESTAMP_FORMAT)

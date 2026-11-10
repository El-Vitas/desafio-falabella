from enum import StrEnum


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


class ColumnKind(StrEnum):
    INTEGER = "integer"
    TEXT = "text"

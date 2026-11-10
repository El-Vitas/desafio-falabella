from enum import StrEnum


class ErrorCode(StrEnum):
    INVALID_REQUEST = "invalid_request"
    NOT_FOUND = "not_found"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    HTTP_ERROR = "http_error"
    DATA_NOT_LOADED = "data_not_loaded"
    DATABASE_UNAVAILABLE = "database_unavailable"
    INTERNAL_ERROR = "internal_error"


ERROR_CODE_BY_STATUS = {
    404: ErrorCode.NOT_FOUND,
    405: ErrorCode.METHOD_NOT_ALLOWED,
}

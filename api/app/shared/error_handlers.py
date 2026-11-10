import logging

import psycopg
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.shared.constants.error_codes import ERROR_CODE_BY_STATUS, ErrorCode
from app.shared.constants.http import LOCATION_SEPARATOR
from app.shared.schemas import ErrorContent, ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


def error_response(
    status_code: int,
    code: ErrorCode,
    message: str,
    details: list[ErrorDetail] | None = None,
) -> JSONResponse:
    body = ErrorResponse(error=ErrorContent(code=code, message=message, details=details or []))
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


def _validation_detail(error: dict[str, object]) -> ErrorDetail:
    location = error.get("loc", ())
    field = LOCATION_SEPARATOR.join(str(part) for part in location)
    return ErrorDetail(field=field, message=str(error.get("msg", "")))


def _invalid_request(_request: Request, error: RequestValidationError) -> JSONResponse:
    return error_response(
        status.HTTP_400_BAD_REQUEST,
        ErrorCode.INVALID_REQUEST,
        "The request has invalid parameters",
        [_validation_detail(detail) for detail in error.errors()],
    )


def _http_error(_request: Request, error: HTTPException) -> JSONResponse:
    code = ERROR_CODE_BY_STATUS.get(error.status_code, ErrorCode.HTTP_ERROR)
    response = error_response(error.status_code, code, str(error.detail))
    response.headers.update(error.headers or {})
    return response


def _data_not_loaded(_request: Request, error: psycopg.errors.UndefinedTable) -> JSONResponse:
    logger.warning("A query used a table or view that does not exist yet: %s", error)
    return error_response(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        ErrorCode.DATA_NOT_LOADED,
        "The data is not loaded yet; run the pokemon_pipeline DAG",
    )


def _database_unavailable(_request: Request, _error: psycopg.OperationalError) -> JSONResponse:
    logger.exception("The database is unavailable or too slow")
    return error_response(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        ErrorCode.DATABASE_UNAVAILABLE,
        "The database is unavailable, try again later",
    )


def _unexpected_error(_request: Request, _error: Exception) -> JSONResponse:
    logger.exception("Unexpected error while handling a request")
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        ErrorCode.INTERNAL_ERROR,
        "An unexpected error occurred",
    )


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, _invalid_request)
    app.add_exception_handler(HTTPException, _http_error)
    app.add_exception_handler(psycopg.errors.UndefinedTable, _data_not_loaded)
    app.add_exception_handler(psycopg.OperationalError, _database_unavailable)
    app.add_exception_handler(Exception, _unexpected_error)

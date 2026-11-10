from fastapi import status

from app.shared.schemas import ErrorResponse

UNUSED_VALIDATION_STATUS = str(status.HTTP_422_UNPROCESSABLE_CONTENT)
UNUSED_VALIDATION_SCHEMAS = ("HTTPValidationError", "ValidationError")

SERVER_ERROR_RESPONSES: dict[int | str, dict[str, object]] = {
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        "model": ErrorResponse,
        "description": "The database is down or the pipeline has not loaded the data yet",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorResponse,
        "description": "Unexpected error, without internal details",
    },
}

INVALID_REQUEST_RESPONSE: dict[int | str, dict[str, object]] = {
    status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid parameters"},
}

NOT_FOUND_RESPONSE: dict[int | str, dict[str, object]] = {
    status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "The Pokémon does not exist"},
}

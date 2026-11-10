from pydantic import BaseModel

from app.shared.constants.error_codes import ErrorCode


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorContent(BaseModel):
    code: ErrorCode
    message: str
    details: list[ErrorDetail] = []


class ErrorResponse(BaseModel):
    error: ErrorContent

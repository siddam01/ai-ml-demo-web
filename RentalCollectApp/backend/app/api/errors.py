from __future__ import annotations

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.utils.exceptions import AppError


def app_error_handler(_: Request, exc: AppError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.error_code, "message": str(exc)}},
    )


def validation_error_handler(_: Request, exc: RequestValidationError) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Validation failed", "details": exc.errors()}},
    )


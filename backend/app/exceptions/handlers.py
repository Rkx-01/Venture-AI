"""
exceptions/handlers.py
-----------------------
Global FastAPI exception handlers.

Registration
------------
All handlers are registered in register_exception_handlers(app), which
is called once from main.py create_app(). This keeps main.py clean.

Error response shape
--------------------
Every error — validation, HTTP, application, or unhandled — returns the
same JSON envelope:

    {
        "error":   "Human-readable message",
        "code":    "MACHINE_READABLE_CODE",
        "details": { ... }     ← optional: field errors, context
    }

Handler priority (FastAPI processes in this order):
    1. RequestValidationError  (Pydantic schema failures on request body)
    2. AppException            (our custom hierarchy)
    3. HTTPException           (FastAPI/Starlette built-in)
    4. Exception               (anything else — last resort)
"""

from __future__ import annotations
from typing import Optional

import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.custom_exceptions import AppException
from app.utils.logger import get_logger

logger = get_logger("api.errors")


# ---------------------------------------------------------------------------
# Response factory
# ---------------------------------------------------------------------------


def _error_response(
    *,
    status_code: int,
    error: str,
    code: str,
    details: dict[str, Optional[Any]] = None,
    request_id: Optional[str] = None,
) -> JSONResponse:
    """
    Builds a consistent error JSON response.

    Args:
        status_code:  HTTP status code.
        error:        Human-readable message shown to API consumers.
        code:         Machine-readable error type (e.g. "NOT_FOUND").
        details:      Optional additional context (field errors, ids, etc.).
        request_id:   Propagated X-Request-ID for log correlation.
    """
    body: dict[str, Any] = {"error": error, "code": code}
    if details:
        body["details"] = details

    headers = {}
    if request_id:
        headers["X-Request-ID"] = request_id

    return JSONResponse(status_code=status_code, content=body, headers=headers)


def _request_id(request: Request) -> Optional[str]:
    """Extract the request ID injected by LoggingMiddleware, if present."""
    return request.headers.get("X-Request-ID")


# ---------------------------------------------------------------------------
# Handler: Pydantic request validation errors  (422)
# ---------------------------------------------------------------------------


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handles FastAPI/Pydantic validation failures on incoming request bodies,
    path parameters, and query strings.

    Transforms the verbose Pydantic error list into a compact, field-keyed
    dictionary so clients know exactly which field failed and why.

    Example response:
        {
            "error": "Request validation failed",
            "code": "VALIDATION_ERROR",
            "details": {
                "body.idea_text": "Field required",
                "body.industry": "String should have at most 100 characters"
            }
        }
    """
    field_errors: dict[str, str] = {}
    for err in exc.errors():
        # loc is a tuple like ("body", "idea_text") or ("query", "page")
        field = ".".join(str(part) for part in err["loc"])
        field_errors[field] = err["msg"]

    logger.warning(
        "Request validation failed | %s %s | %d field(s)",
        request.method,
        request.url.path,
        len(field_errors),
        extra={"validation_errors": field_errors, "request_id": _request_id(request)},
    )

    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error="Request validation failed",
        code="VALIDATION_ERROR",
        details=field_errors,
        request_id=_request_id(request),
    )


# ---------------------------------------------------------------------------
# Handler: Custom AppException hierarchy
# ---------------------------------------------------------------------------


async def app_exception_handler(
    request: Request, exc: AppException
) -> JSONResponse:
    """
    Handles any exception that inherits from AppException.

    Uses the exception's own http_status and code, keeping the handler
    completely generic — adding a new exception subclass requires zero
    changes here.
    """
    log_level = (
        logging.ERROR
        if exc.http_status >= 500
        else logging.WARNING
        if exc.http_status >= 400
        else logging.INFO
    )
    logger.log(
        log_level,
        "%s raised | %s %s | %s",
        type(exc).__name__,
        request.method,
        request.url.path,
        exc.message,
        extra={
            "error_code": exc.code,
            "request_id": _request_id(request),
            **exc.context,
        },
    )

    return _error_response(
        status_code=exc.http_status,
        error=exc.message,
        code=exc.code,
        details=exc.context if exc.context else None,
        request_id=_request_id(request),
    )


# ---------------------------------------------------------------------------
# Handler: FastAPI / Starlette HTTPException
# ---------------------------------------------------------------------------


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """
    Handles standard FastAPI HTTPExceptions (e.g. raised by Depends, security).
    Maps the status code to a generic code string for machine-readability.
    """
    CODE_MAP: dict[int, str] = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_ERROR",
        503: "SERVICE_UNAVAILABLE",
    }
    code = CODE_MAP.get(exc.status_code, "HTTP_ERROR")

    logger.warning(
        "HTTPException | %s %s | %d",
        request.method,
        request.url.path,
        exc.status_code,
        extra={"error_code": code, "request_id": _request_id(request)},
    )

    return _error_response(
        status_code=exc.status_code,
        error=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        code=code,
        request_id=_request_id(request),
    )


# ---------------------------------------------------------------------------
# Handler: Unhandled exceptions  (500 catch-all)
# ---------------------------------------------------------------------------


async def unhandled_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """
    Safety net — catches any exception not handled above.

    Always returns 500. Full traceback is logged but NOT included in the
    response body (leaking stack traces to clients is a security risk).
    """
    logger.error(
        "Unhandled exception | %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
        extra={"request_id": _request_id(request)},
    )

    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error="An unexpected error occurred. Please try again later.",
        code="INTERNAL_ERROR",
        request_id=_request_id(request),
    )


# ---------------------------------------------------------------------------
# Registration helper — called once from create_app()
# ---------------------------------------------------------------------------


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers all global exception handlers on the FastAPI application.

    Call this inside create_app() after the app instance is created.
    Order matters: FastAPI matches the most specific type first.
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

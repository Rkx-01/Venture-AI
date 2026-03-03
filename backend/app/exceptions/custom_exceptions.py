"""
exceptions/custom_exceptions.py
--------------------------------
Application-specific exception hierarchy.

Design
------
All custom exceptions inherit from AppException, which carries:
  - message   Human-readable error description
  - code      Machine-readable error type string (used in API responses)
  - http_status  The HTTP status code the handler should return

Raising an AppException anywhere in the service layer will produce a
consistent JSON response via the global handler in handlers.py.

Usage
-----
    from app.exceptions.custom_exceptions import NotFoundError, ValidationError

    raise NotFoundError("Startup idea not found", resource_id=idea_id)
"""

from __future__ import annotations
from typing import Any

from http import HTTPStatus


# ---------------------------------------------------------------------------
# Base exception
# ---------------------------------------------------------------------------


class AppException(Exception):
    """
    Base class for all application-level errors.

    All subclasses must define a default `code` and `http_status`.
    Extra keyword arguments are stored in `context` and included in
    structured error responses for debugging.
    """

    code: str = "INTERNAL_ERROR"
    http_status: int = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str, **context: Any) -> None:
        super().__init__(message)
        self.message = message
        self.context = context  # e.g. resource_id=42, field="email"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(code={self.code!r}, message={self.message!r})"


# ---------------------------------------------------------------------------
# 400 — Bad Request
# ---------------------------------------------------------------------------


class BadRequestError(AppException):
    """The request is malformed or contains invalid data."""
    code = "BAD_REQUEST"
    http_status = HTTPStatus.BAD_REQUEST


# ---------------------------------------------------------------------------
# 401 — Unauthorized
# ---------------------------------------------------------------------------


class UnauthorizedError(AppException):
    """The request lacks valid authentication credentials."""
    code = "UNAUTHORIZED"
    http_status = HTTPStatus.UNAUTHORIZED


# ---------------------------------------------------------------------------
# 403 — Forbidden
# ---------------------------------------------------------------------------


class ForbiddenError(AppException):
    """The authenticated user does not have permission."""
    code = "FORBIDDEN"
    http_status = HTTPStatus.FORBIDDEN


# ---------------------------------------------------------------------------
# 404 — Not Found
# ---------------------------------------------------------------------------


class NotFoundError(AppException):
    """The requested resource does not exist."""
    code = "NOT_FOUND"
    http_status = HTTPStatus.NOT_FOUND


# ---------------------------------------------------------------------------
# 409 — Conflict
# ---------------------------------------------------------------------------


class ConflictError(AppException):
    """The request conflicts with the current state of the resource."""
    code = "CONFLICT"
    http_status = HTTPStatus.CONFLICT


# ---------------------------------------------------------------------------
# 422 — Unprocessable Entity (business-logic validation, not Pydantic)
# ---------------------------------------------------------------------------


class BusinessValidationError(AppException):
    """
    Business rule violation that cannot be caught by schema validation.

    Example: "An idea in 'processing' state cannot be deleted."
    """
    code = "BUSINESS_VALIDATION_ERROR"
    http_status = HTTPStatus.UNPROCESSABLE_ENTITY


# ---------------------------------------------------------------------------
# 429 — Too Many Requests
# ---------------------------------------------------------------------------


class RateLimitError(AppException):
    """The client has exceeded the allowed request rate."""
    code = "RATE_LIMIT_EXCEEDED"
    http_status = HTTPStatus.TOO_MANY_REQUESTS


# ---------------------------------------------------------------------------
# 503 — Service Unavailable (external service failures)
# ---------------------------------------------------------------------------


class ExternalServiceError(AppException):
    """
    A downstream service (OpenAI, Pinecone, etc.) returned an error
    or is unavailable.
    """
    code = "EXTERNAL_SERVICE_ERROR"
    http_status = HTTPStatus.SERVICE_UNAVAILABLE


# ---------------------------------------------------------------------------
# 500 — Internal Server Error
# ---------------------------------------------------------------------------


class InternalError(AppException):
    """Generic internal server error — wrap truly unexpected failures."""
    code = "INTERNAL_ERROR"
    http_status = HTTPStatus.INTERNAL_SERVER_ERROR

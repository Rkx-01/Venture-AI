from __future__ import annotations
# exceptions/__init__.py
from app.exceptions.custom_exceptions import (  # noqa: F401
    AppException,
    BadRequestError,
    BusinessValidationError,
    ConflictError,
    ExternalServiceError,
    ForbiddenError,
    InternalError,
    NotFoundError,
    RateLimitError,
    UnauthorizedError,
)
from app.exceptions.handlers import register_exception_handlers  # noqa: F401

__all__ = [
    # Base
    "AppException",
    # 4xx
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "ConflictError",
    "BusinessValidationError",
    "RateLimitError",
    # 5xx
    "ExternalServiceError",
    "InternalError",
    # Registration
    "register_exception_handlers",
]

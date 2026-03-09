"""
utils/logger.py
---------------
Centralised logging configuration for the AI Startup Analyst API.

Features
--------
- Structured log format: timestamp | level | module | message
- Optional JSON formatter (active in production) for log aggregators
  (Datadog, CloudWatch, GCP Logging, etc.)
- Rotating file handler — keeps logs on disk, auto-rotates at 10 MB,
  retains the last 5 files.
- Console handler — always active, coloured output in development.
- Per-logger granular level control.
- Noisy third-party loggers suppressed by default.

Usage
-----
Call setup_logging() exactly once at app startup (in main.py lifespan).

    from app.utils.logger import setup_logging, get_logger
    setup_logging()

    logger = get_logger(__name__)
    logger.info("Server started")
    logger.error("Something went wrong", exc_info=True)
"""
from __future__ import annotations

import json
import logging
import logging.handlers
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config.settings import get_settings

settings = get_settings()

# ---------------------------------------------------------------------------
# Log directory
# ---------------------------------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "api.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

CONSOLE_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
)
CONSOLE_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class JSONFormatter(logging.Formatter):
    """
    Emits one JSON object per log line.

    Field set:
        timestamp   ISO-8601 UTC
        level       DEBUG / INFO / WARNING / ERROR / CRITICAL
        logger      Dotted module path (e.g. app.middleware.logging)
        message     Log message string
        endpoint    Present on request logs (injected via extra={})
        duration_ms Present on request logs (injected via extra={})
        status_code Present on request logs (injected via extra={})
        request_id  Present on request logs (injected via extra={})
        exc_info    Serialised traceback (only when an exception is logged)
    """

    # Fields that belong to the LogRecord internals — exclude from output
    _SKIP_FIELDS = frozenset({
        "msg", "args", "levelno", "pathname", "filename", "module",
        "exc_info", "exc_text", "stack_info", "lineno", "funcName",
        "created", "msecs", "relativeCreated", "thread", "threadName",
        "processName", "process", "taskName",
    })

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Append any extra fields injected via logger.info(..., extra={...})
        for key, value in record.__dict__.items():
            if key not in self._SKIP_FIELDS and not key.startswith("_"):
                payload[key] = value

        # Serialise exception traceback if present
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def setup_logging() -> None:
    """
    Configure the root logger and attach all handlers.

    Call exactly once during application startup.
    In development: coloured console output.
    In production:  JSON console output + rotating file handlers.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.is_debug else logging.INFO)

    # Remove any handlers added by earlier basicConfig() calls
    root_logger.handlers.clear()

    # -- Console handler ---------------------------------------------------
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.is_production:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(
            logging.Formatter(CONSOLE_FORMAT, datefmt=CONSOLE_DATE_FORMAT)
        )
    console_handler.setLevel(logging.DEBUG if settings.is_debug else logging.INFO)
    root_logger.addHandler(console_handler)

    # -- Rotating all-log file handler (production only) -------------------
    if settings.is_production:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,   # 10 MB per file
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(JSONFormatter())
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)

        # -- Rotating error-only file handler ------------------------------
        error_handler = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        error_handler.setFormatter(JSONFormatter())
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)

    # -- Suppress noisy third-party loggers --------------------------------
    _SUPPRESSED_LOGGERS = {
        "uvicorn.access": logging.WARNING,
        "httpx": logging.WARNING,
        "sqlalchemy.engine": logging.WARNING if not settings.is_debug else logging.INFO,
        "asyncio": logging.WARNING,
    }
    for name, level in _SUPPRESSED_LOGGERS.items():
        logging.getLogger(name).setLevel(level)

    logging.getLogger(__name__).info(
        "Logging initialised | env=%s | level=%s | json=%s",
        settings.ENVIRONMENT.value,
        logging.getLevelName(root_logger.level),
        settings.is_production,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger scoped to the calling module.

    Usage:
        # At the top of any module:
        logger = get_logger(__name__)
        logger.info("Startup complete")
        logger.error("DB failed", exc_info=True)
    """
    return logging.getLogger(name)

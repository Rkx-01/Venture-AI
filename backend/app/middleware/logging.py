"""
middleware/logging.py
---------------------
Request logging middleware — logs every incoming request and outgoing
response with structured fields:

    timestamp     ISO-8601 UTC (from logger)
    level         INFO on success, WARNING on 4xx, ERROR on 5xx
    endpoint      HTTP method + path (e.g. "GET /health")
    status_code   HTTP response code
    duration_ms   End-to-end processing time in milliseconds
    request_id    Short UUID injected into X-Request-ID response header
    client_ip     Caller IP address
    user_agent    Caller User-Agent header

Error bodies are captured and logged separately at ERROR level so they
appear in the structured error log file too.
"""
from __future__ import annotations

import time
import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import get_logger

logger = get_logger("api.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Starlette middleware that emits one structured log line per request.

    Log level is chosen by response status:
        2xx / 3xx  → INFO
        4xx        → WARNING  (client error — not our fault, but worth tracking)
        5xx        → ERROR    (server error — needs attention)
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())[:8]

        # --- Capture request metadata before forwarding ---
        method = request.method
        path = request.url.path
        query = str(request.url.query)
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "-")
        endpoint = f"{method} {path}"

        start_ns = time.perf_counter_ns()

        # --- Process the request ---
        try:
            response = await call_next(request)
        except Exception as exc:
            # Unhandled exception — log at CRITICAL and re-raise
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            logger.critical(
                "Unhandled exception during request",
                extra={
                    "request_id": request_id,
                    "endpoint": endpoint,
                    "client_ip": client_ip,
                    "duration_ms": round(duration_ms, 3),
                },
                exc_info=exc,
            )
            raise

        # --- Compute duration ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        status_code = response.status_code

        # --- Choose log level based on status code ---
        log_extra = {
            "request_id": request_id,
            "endpoint": endpoint,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 3),
            "client_ip": client_ip,
            "user_agent": user_agent,
        }
        if query:
            log_extra["query"] = query

        log_message = (
            f"{endpoint} | {status_code} | {duration_ms:.2f}ms | [{request_id}]"
        )

        if status_code >= 500:
            logger.error(log_message, extra=log_extra)
        elif status_code >= 400:
            logger.warning(log_message, extra=log_extra)
        else:
            logger.info(log_message, extra=log_extra)

        # Inject the request ID into the response for client-side correlation
        response.headers["X-Request-ID"] = request_id
        return response

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """
        Extracts real client IP, respecting X-Forwarded-For from proxies/LBs.
        Falls back to the direct connection address.
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            # X-Forwarded-For can be a comma-separated list: "client, proxy1, proxy2"
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

"""
middleware/rate_limiter.py
--------------------------
Token Bucket Rate Limiting Middleware.

Limits traffic per client IP address.

Implementation:
- Token Bucket algorithm (Memory-backed for this starter).
- Capable of being easily swapped to Redis for horizontal scalability.
- 100 requests per minute by default.

Returns:
- 429 Too Many Requests
- Body: {"error": "Rate limit exceeded"}
"""
from __future__ import annotations
from typing import Dict, Tuple

import time
from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import get_logger

logger = get_logger("api.ratelimit")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to rate limit requests per IP address using a Token Bucket.
    
    Default: 100 requests / 60 seconds.
    
    Note: In a multi-worker production environment (e.g., Gunicorn with 4 workers), 
    this simple memory dict implies each worker has its own bucket.
    To enforce a strict global limit across all workers/pods, replace `_buckets` 
    with a Redis client (e.g., aioredis) using the same logic.
    """

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.capacity = max_requests
        self.refill_rate = max_requests / window_seconds
        
        # State: { "ip_address": (tokens_remaining, last_refill_timestamp) }
        self._buckets: Dict[str, Tuple[float, float]] = {}

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = self._get_client_ip(request)
        now = time.monotonic()

        # Init or retrieve bucket
        if client_ip not in self._buckets:
            tokens = self.capacity
            last_refill = now
        else:
            tokens, last_refill = self._buckets[client_ip]

        # Refill tokens based on elapsed time
        elapsed = now - last_refill
        tokens += elapsed * self.refill_rate
        if tokens > self.capacity:
            tokens = self.capacity

        if tokens >= 1.0:
            # Allow request, consume 1 token
            self._buckets[client_ip] = (tokens - 1.0, now)
            return await call_next(request)
        else:
            # Deny request
            self._buckets[client_ip] = (tokens, now)
            logger.warning(
                "Rate limit exceeded",
                extra={
                    "client_ip": client_ip,
                    "endpoint": f"{request.method} {request.url.path}",
                },
            )
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """Extracts real client IP, respecting proxies/load balancers."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

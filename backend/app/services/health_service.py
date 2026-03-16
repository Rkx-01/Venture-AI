from __future__ import annotations
from app.schemas.health import HealthResponse


class HealthService:
    @staticmethod
    def get_status() -> HealthResponse:
        """Returns the current health status of the application."""
        return HealthResponse(status="ok")

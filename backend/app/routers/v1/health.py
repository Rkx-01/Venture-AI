"""
routers/v1/health.py
--------------------
Health check endpoint — intentionally lives outside /api/v*
because it is an infrastructure concern, not an API feature.
Mounted directly in main.py without a version prefix.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the current operational status of the API.",
)
async def health_check() -> HealthResponse:
    return HealthService.get_status()

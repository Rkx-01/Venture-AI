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

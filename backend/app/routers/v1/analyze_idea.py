from fastapi import APIRouter, HTTPException, status
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_410_GONE,
    summary="[Deprecated] Analyze a startup idea",
    description="This endpoint is deprecated. Use POST /api/evaluate-startup instead.",
)
async def analyze_idea():
    """Deprecated endpoint. Redirects to the new evaluation pipeline."""
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="This endpoint has been deprecated. Use POST /api/evaluate-startup for full analysis."
    )

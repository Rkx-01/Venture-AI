"""
routers/analysis.py
-------------------
Router for the startup idea analysis endpoints.

Routes
------
POST /api/v1/analyze   — Submit a startup idea for AI analysis
GET  /api/v1/analyze/{analysis_id}  — Poll for analysis results (stub)
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.exceptions import NotFoundError
from app.schemas.idea_schema import AnalyzeIdeaRequest, AnalyzeIdeaResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post(
    "",
    response_model=AnalyzeIdeaResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit a startup idea for analysis",
    description=(
        "Accepts a startup idea description and queues it for AI-powered "
        "market research, competitor analysis, and feasibility scoring. "
        "Returns an `analysis_id` to poll for results."
    ),
)
async def submit_idea(
    payload: AnalyzeIdeaRequest,
    db: AsyncSession = Depends(get_db),
) -> AnalyzeIdeaResponse:
    """
    Validates the incoming request (Pydantic), persists the job,
    and returns a 202 Accepted with a tracking ID.

    The heavy AI work is handled asynchronously by the AI engine service.
    """
    analysis_id = uuid.uuid4()
    submitted_at = datetime.now(timezone.utc)

    logger.info(
        "Idea submitted for analysis",
        extra={
            "analysis_id": str(analysis_id),
            "industry": payload.industry,
            "idea_length": len(payload.idea_text),
        },
    )

    # TODO: persist to DB and enqueue AI engine job
    # await AnalysisRepository(db).create(
    #     id=analysis_id, idea_text=payload.idea_text, industry=payload.industry
    # )

    return AnalyzeIdeaResponse(
        analysis_id=analysis_id,
        status="pending",
        message="Your startup idea has been queued for analysis.",
        submitted_at=submitted_at,
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalyzeIdeaResponse,
    summary="Get analysis status",
    description="Poll for the current status of a submitted analysis job.",
)
async def get_analysis_status(
    analysis_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> AnalyzeIdeaResponse:
    """
    Returns the current status of an analysis job by ID.
    Raises 404 if the ID is not found.
    """
    # TODO: fetch from DB
    # record = await AnalysisRepository(db).get(analysis_id)
    # if not record:
    #     raise NotFoundError("Analysis not found", analysis_id=str(analysis_id))

    raise NotFoundError(
        "Analysis not found",
        analysis_id=str(analysis_id),
    )

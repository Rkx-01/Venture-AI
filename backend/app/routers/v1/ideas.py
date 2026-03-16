"""
routers/v1/ideas.py
-------------------
Handles fetching the historical list of analyzed startup ideas.
"""
from __future__ import annotations
from typing import List


from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db
from app.schemas.idea_schema import IdeaResponse
from app.services.idea_repository import IdeaRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "",
    response_model=List[IdeaResponse],
    status_code=status.HTTP_200_OK,
    summary="List analyzed startup ideas",
    description="Fetches a paginated list of analyzed startup ideas sorted by creation date.",
)
async def list_ideas(
    limit: int = Query(50, ge=1, le=100, description="Max number of records to return."),
    offset: int = Query(0, ge=0, description="Number of records to skip."),
    db: AsyncSession = Depends(get_db),
) -> List[IdeaResponse]:
    """
    Fetch all analyzed startup ideas with pagination.
    """
    if db is None:
        logger.info("USE_MOCK_DB is enabled; returning mock ideas.")
        import uuid
        from datetime import datetime
        return [
            IdeaResponse(
                id=uuid.uuid4(),
                idea_text="AI-driven mental health platform for students.",
                industry="HealthTech",
                target_users="University students",
                problem="Lack of affordable mental health support.",
                solution_type="Mobile App",
                revenue_model="B2C Subscription",
                created_at=datetime.utcnow()
            ),
            IdeaResponse(
                id=uuid.uuid4(),
                idea_text="Decentralized identity management for enterprises.",
                industry="FinTech",
                target_users="Large corporations",
                problem="Identity theft and data breaches.",
                solution_type="SaaS Platform",
                revenue_model="B2B License",
                created_at=datetime.utcnow()
            )
        ]

    logger.info("Fetching ideas list from database", extra={"limit": limit, "offset": offset})
    
    repo = IdeaRepository(db)
    ideas = await repo.list_ideas(limit=limit, offset=offset)
    
    return list(ideas)

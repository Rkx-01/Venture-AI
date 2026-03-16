"""
services/idea_repository.py
---------------------------
Data Access service for Startup Ideas.
Encapsulates all database operations relating to the StartupIdea model.
"""
from __future__ import annotations
from typing import Optional

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.startup_idea import StartupIdea
from app.utils.logger import get_logger

logger = get_logger(__name__)


class IdeaRepository:
    """
    Repository for creating, reading, and updating startup ideas in the DB.
    Requires an active SQLAlchemy AsyncSession.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_idea(
        self,
        idea_text: str,
        industry: str,
        target_users: Optional[str] = None,
        problem: Optional[str] = None,
        solution_type: Optional[str] = None,
        revenue_model: Optional[str] = None,
    ) -> StartupIdea:
        """
        Creates a new StartupIdea record in the database.
        
        Args:
            idea_text: Original raw idea.
            industry: User-provided or AI-inferred industry.
            target_users: The demographic extracted from analysis.
            problem: The core issue being solved.
            solution_type: The format of the solution.
            revenue_model: Revenue mechanism.
            
        Returns:
            The fully persisted StartupIdea ORM instance.
        """
        idea = StartupIdea(
            idea_text=idea_text,
            industry=industry,
            target_users=target_users,
            problem=problem,
            solution_type=solution_type,
            revenue_model=revenue_model,
        )

        self.session.add(idea)
        await self.session.commit()
        await self.session.refresh(idea)
        
        logger.debug("Persisted StartupIdea with ID %s to database.", idea.id)
        return idea

    async def get_idea_by_id(self, idea_id: uuid.UUID) -> Optional[StartupIdea]:
        """
        Fetches a StartupIdea by its primary key.
        """
        query = select(StartupIdea).where(StartupIdea.id == idea_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_ideas(self, limit: int = 50, offset: int = 0) -> Sequence[StartupIdea]:
        """
        Returns a paginated list of analyzed startup ideas.
        """
        query = select(StartupIdea).order_by(StartupIdea.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

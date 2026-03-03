"""
repositories/startup_score_repository.py
----------------------------------------
Data Access service for Startup Score results.
"""
from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.startup_score import StartupScore
from app.utils.logger import get_logger

logger = get_logger(__name__)


class StartupScoreRepository:
    """
    Repository for creating and retrieving startup score records in the DB.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_score(
        self,
        startup_idea_id: uuid.UUID,
        market_potential_score: int,
        competition_score: int,
        scalability_score: int,
        execution_risk_score: int,
        overall_score: float,
        success_probability: str
    ) -> StartupScore:
        """
        Persists a startup viability score result to the database.
        """
        score_record = StartupScore(
            startup_idea_id=startup_idea_id,
            market_potential_score=market_potential_score,
            competition_score=competition_score,
            scalability_score=scalability_score,
            execution_risk_score=execution_risk_score,
            overall_score=overall_score,
            success_probability=success_probability
        )

        self.session.add(score_record)
        await self.session.commit()
        await self.session.refresh(score_record)
        
        logger.debug("Persisted StartupScore for idea %s", startup_idea_id)
        return score_record

    async def get_score_by_idea(self, idea_id: uuid.UUID) -> Sequence[StartupScore]:
        """
        Retrieves all score records associated with a specific startup idea.
        """
        query = select(StartupScore).where(StartupScore.startup_idea_id == idea_id).order_by(StartupScore.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_scores(self) -> Sequence[StartupScore]:
        """
        Retrieves all historical startup score records.
        """
        query = select(StartupScore).order_by(StartupScore.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

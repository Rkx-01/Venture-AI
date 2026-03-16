"""
services/market_repository.py
----------------------------
Data Access service for Market Analysis results.
"""
from __future__ import annotations

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.market_analysis import MarketAnalysis
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MarketRepository:
    """
    Repository for creating and retrieving market analysis records in the DB.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_market_analysis(
        self,
        startup_idea_id: uuid.UUID,
        tam: str,
        sam: str,
        som: str,
        industry_growth_rate: str,
        market_opportunity_score: int,
    ) -> MarketAnalysis:
        """
        Persists a market analysis result to the database.
        """
        analysis = MarketAnalysis(
            startup_idea_id=startup_idea_id,
            tam=tam,
            sam=sam,
            som=som,
            industry_growth_rate=industry_growth_rate,
            market_opportunity_score=market_opportunity_score,
        )

        self.session.add(analysis)
        await self.session.commit()
        await self.session.refresh(analysis)
        
        logger.debug("Persisted MarketAnalysis for idea %s", startup_idea_id)
        return analysis

    async def get_analysis_by_idea(self, idea_id: uuid.UUID) -> Sequence[MarketAnalysis]:
        """
        Retrieves all market analysis records associated with a specific startup idea.
        """
        query = select(MarketAnalysis).where(MarketAnalysis.startup_idea_id == idea_id).order_by(MarketAnalysis.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_market_analyses(self) -> Sequence[MarketAnalysis]:
        """
        Retrieves all historical market analysis records.
        """
        query = select(MarketAnalysis).order_by(MarketAnalysis.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

"""
services/competitor_repository.py
---------------------------------
Data Access service for Competitor intelligence.
"""
from __future__ import annotations
from typing import List

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.competitor import Competitor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CompetitorRepository:
    """
    Repository for persisting and retrieving competitor data in the database.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_competitors(
        self,
        startup_idea_id: uuid.UUID,
        competitors_list: List[dict]
    ) -> List[Competitor]:
        """
        Persists a list of competitors for a given startup idea.
        
        Args:
            startup_idea_id: The ID of the parent startup idea.
            competitors_list: List of dicts matching the Competitor model schema.
        """
        logger.info("Saving %d competitors for idea %s", len(competitors_list), startup_idea_id)
        
        results = []
        for comp_data in competitors_list:
            competitor = Competitor(
                startup_idea_id=startup_idea_id,
                name=comp_data.get("name"),
                description=comp_data.get("description"),
                target_market=comp_data.get("market_focus"), # Map from AI field to DB field
                pricing_model=comp_data.get("pricing_model"),
                strengths=comp_data.get("strengths"),
                weaknesses=comp_data.get("weaknesses")
            )
            self.session.add(competitor)
            results.append(competitor)

        await self.session.commit()
        # Refreshing all isn't strictly necessary unless we need IDs immediately
        logger.debug("Successfully persisted competitors for idea %s", startup_idea_id)
        return results

    async def get_competitors_by_idea(self, idea_id: uuid.UUID) -> Sequence[Competitor]:
        """
        Retrieves all competitors associated with a specific startup idea.
        """
        query = select(Competitor).where(Competitor.startup_idea_id == idea_id).order_by(Competitor.name.asc())
        result = await self.session.execute(query)
        return result.scalars().all()

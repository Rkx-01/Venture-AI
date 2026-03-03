"""
repositories/report_repository.py
----------------------------------
Data Access service for synthesized Startup Reports.
"""
from __future__ import annotations
from typing import Optional

import uuid
from typing import Sequence, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.startup_report import StartupReport
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReportRepository:
    """
    Repository for creating and retrieving reports in the DB.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_report(
        self,
        startup_idea_id: uuid.UUID,
        executive_summary: str,
        problem_solution_analysis: str,
        market_opportunity: str,
        competitor_landscape: str,
        startup_score_summary: str,
        markdown_content: str,
        generation_metadata: Dict[str, Optional[Any]] = None
    ) -> StartupReport:
        """
        Persists a generated report to the database.
        """
        report_record = StartupReport(
            startup_idea_id=startup_idea_id,
            executive_summary=executive_summary,
            problem_solution_analysis=problem_solution_analysis,
            market_opportunity=market_opportunity,
            competitor_landscape=competitor_landscape,
            startup_score_summary=startup_score_summary,
            markdown_content=markdown_content,
            generation_metadata=generation_metadata
        )

        self.session.add(report_record)
        await self.session.commit()
        await self.session.refresh(report_record)
        
        logger.debug("Persisted StartupReport %s for idea %s", report_record.id, startup_idea_id)
        return report_record

    async def get_by_id(self, report_id: uuid.UUID) -> Optional[StartupReport]:
        """
        Retrieves a specific report by its unique ID.
        """
        query = select(StartupReport).where(StartupReport.id == report_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_report_by_idea(self, idea_id: uuid.UUID) -> Sequence[StartupReport]:
        """
        Retrieves all report records associated with a specific startup idea.
        """
        query = select(StartupReport).where(StartupReport.startup_idea_id == idea_id).order_by(StartupReport.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_reports(self) -> Sequence[StartupReport]:
        """
        Retrieves all historical startup report records.
        """
        query = select(StartupReport).order_by(StartupReport.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

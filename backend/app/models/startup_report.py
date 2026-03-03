"""
models/report.py
----------------
SQLAlchemy model for storing generated startup reports.
"""
from __future__ import annotations

from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base, UUIDMixin, TimestampMixin


class StartupReport(Base, UUIDMixin, TimestampMixin):
    """
    Represents a synthesized professional report for a startup idea.
    Stores the narrative sections and the final markdown/metadata.
    """
    __tablename__ = "startup_reports"

    startup_idea_id = Column(UUID(as_uuid=True), ForeignKey("startup_ideas.id"), nullable=False, index=True)
    
    # Narrative sections
    executive_summary = Column(String, nullable=False)
    problem_solution_analysis = Column(String, nullable=False)
    market_opportunity = Column(String, nullable=False)
    competitor_landscape = Column(String, nullable=False)
    startup_score_summary = Column(String, nullable=False)
    
    # Export formats (Keeping for our robust export service)
    markdown_content = Column(String, nullable=False)
    
    # Metadata / Settings used for generation
    generation_metadata = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<StartupReport(id={self.id}, startup_idea_id={self.startup_idea_id})>"

"""
schemas/report_schema.py
-----------------------
Pydantic schemas for startup report generation requests.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ReportGenerationRequest(BaseModel):
    """
    Request model for triggering a comprehensive startup report generation.
    """
    startup_idea_id: uuid.UUID = Field(description="The unique ID of the startup idea to report on.")


class ReportResponse(BaseModel):
    """
    Schema for representing a fetched Report in the collection.
    """
    id: uuid.UUID
    startup_idea_id: uuid.UUID
    executive_summary: str
    problem_solution_analysis: str
    market_opportunity: str
    competitor_landscape: str
    startup_score_summary: str
    markdown_content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

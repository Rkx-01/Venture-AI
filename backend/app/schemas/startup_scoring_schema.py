"""
schemas/startup_scoring_schema.py
---------------------------------
Pydantic schemas for startup viability scoring requests.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class StartupScoringRequest(BaseModel):
    """
    Request model for triggering a startup viability assessment.
    """
    startup_idea_id: uuid.UUID = Field(description="The unique ID of the startup idea to score.")


class StartupScoreResponse(BaseModel):
    """
    Schema for representing a fetched Startup Score in the collection.
    """
    id: uuid.UUID
    startup_idea_id: uuid.UUID
    market_potential_score: int
    competition_score: int
    scalability_score: int
    execution_risk_score: int
    overall_score: float
    success_probability: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

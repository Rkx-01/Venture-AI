"""
schemas/market_schema.py
------------------------
Pydantic schemas for the market analysis endpoints.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class MarketAnalysisRequest(BaseModel):
    """
    Request body for POST /api/v1/market-analysis.
    """
    industry: str = Field(..., description="Target industry to analyse.", examples=["HealthTech"])
    target_users: str = Field(..., description="Target users for the startup idea.", examples=["College students"])
    solution_type: str = Field(..., description="The format of the solution.", examples=["AI mental health assistant"])

    model_config = {
        "json_schema_extra": {
            "example": {
                "industry": "HealthTech",
                "target_users": "College students",
                "solution_type": "AI mental health assistant"
            }
        }
    }


class IndustryTrendRequest(BaseModel):
    """
    Request body for POST /api/v1/market-analysis/trends.
    """
    industry: str = Field(..., description="The name of the industry to analyze.", examples=["HealthTech"])


class MarketAnalysisResponse(BaseModel):
    """
    Schema for representing a fetched Market Analysis in the collection.
    """
    id: uuid.UUID
    startup_idea_id: uuid.UUID
    tam: str
    sam: str
    som: str
    industry_growth_rate: str
    market_opportunity_score: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


"""
schemas/competitor_schema.py
----------------------------
Pydantic schemas for competitor analysis requests and responses.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class CompetitorAnalysisRequest(BaseModel):
    """
    Request schema for competitor analysis.
    """
    idea_text: str = Field(
        ..., 
        min_length=10, 
        description="The startup idea text to analyze for competitors."
    )
    industry: str = Field(
        ..., 
        min_length=3, 
        description="The primary industry sector."
    )

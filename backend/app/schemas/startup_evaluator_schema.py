from pydantic import BaseModel, Field
from typing import List


class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class MarketInsights(BaseModel):
    tam: str
    sam: str
    som: str
    trends: str


class CompetitorDetail(BaseModel):
    name: str
    description: str = ""
    # Accept both singular and plural forms from the LLM
    strengths: str = Field(default="", alias="strengths")
    weaknesses: str = Field(default="", alias="weaknesses")

    model_config = {"populate_by_name": True}


class EvaluateStartupResponse(BaseModel):
    idea_summary: str
    target_users: str
    market_insights: MarketInsights
    competitors: List[CompetitorDetail]
    swot: SWOTAnalysis
    startup_score: float
    investment_recommendation: str = ""
    report: str = ""

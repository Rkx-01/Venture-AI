from fastapi import APIRouter

from app.routers.v1 import (
    analyze_idea,
    competitor_analysis,
    ideas,
    market_analysis,
    startup_scoring,
    report_generation,
)

v1_router = APIRouter()

v1_router.include_router(analyze_idea.router, prefix="/analyze-idea", tags=["Analyze Idea"])
v1_router.include_router(market_analysis.router, prefix="/market-analysis", tags=["Market Analysis"])
v1_router.include_router(ideas.router, prefix="/ideas", tags=["Ideas"])
v1_router.include_router(competitor_analysis.router, prefix="/competitor-analysis", tags=["Competitor Analysis"])
v1_router.include_router(startup_scoring.router, prefix="/startup-score", tags=["Startup Scoring"])
v1_router.include_router(report_generation.router, prefix="/reports", tags=["Report Generation"])

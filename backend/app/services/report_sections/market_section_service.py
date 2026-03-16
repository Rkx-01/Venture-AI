"""
services/report_sections/market_section_service.py
--------------------------------------------------
Modular service for generating the market opportunity section of the report.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MarketSectionResult(BaseModel):
    """
    Structured output for the market opportunity section.
    """
    market_opportunity: str = Field(description="A strategic and quantitative analysis of the market opportunity.")


class MarketSectionService:
    """
    Specialized service to generate data-driven market opportunity narratives.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_market_section(
        self,
        tam: str,
        sam: str,
        som: str,
        industry_growth_rate: str,
        market_opportunity_score: int
    ) -> MarketSectionResult:
        """
        Generates a strategic market opportunity analysis.
        """
        logger.info("Generating market opportunity analysis for SAM: %s", sam)

        system_prompt = "You are a Market Intelligence Expert and VC Analyst. Provide a data-driven and strategically insightful market analysis."
        
        user_prompt = PromptManager.get_prompt(
            "market_section_prompt",
            tam=tam,
            sam=sam,
            som=som,
            industry_growth_rate=industry_growth_rate,
            market_opportunity_score=market_opportunity_score
        )

        raw_result = await self.llm.generate_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            response_format_json=True
        )

        import json
        data = json.loads(raw_result)
        return MarketSectionResult(**data)

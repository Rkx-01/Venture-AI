"""
services/market_positioning_service.py
--------------------------------------
Service for suggesting strategic market positioning for startup ideas.
"""
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MarketPositioningResult(BaseModel):
    """
    Structured output for recommended market positioning.
    """
    recommended_positioning: str = Field(description="One-sentence strategic positioning statement.")
    competitive_advantage: List[str] = Field(description="List of core competitive moats or advantages.")
    strategic_reasoning: str = Field(description="Justification for the chosen positioning strategy.")


class MarketPositioningService:
    """
    Service to generate high-level strategic positioning recommendations using AI reasoning.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_positioning(
        self, 
        idea_text: str, 
        industry: str, 
        competitors_summary: str
    ) -> MarketPositioningResult:
        """
        Suggests how the startup should position itself to win in its market.

        Args:
            idea_text: description of the startup idea.
            industry: industry classification.
            competitors_summary: High-level overview of the competition.

        Returns:
            Validated MarketPositioningResult.
        """
        logger.info("Generating market positioning strategy for idea in %s", industry)

        system_prompt = (
            "You are a World-Class Startup Strategist and Positioning Expert (inspired by April Dunford). "
            "Your task is to find the unique 'playing field' where this startup can be the dominant player. "
            "Focus on differentiation, category creation, and strategic moats. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "market_positioning_prompt",
            idea_text=idea_text,
            industry=industry,
            competitors_summary=competitors_summary
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.4, # Balanced for creativity and strategic logic
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=MarketPositioningResult,
            max_retries=3
        )

        logger.info("Market positioning strategy generated successfully.")
        return result

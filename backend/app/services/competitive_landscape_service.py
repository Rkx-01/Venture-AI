"""
services/competitive_landscape_service.py
-----------------------------------------
Service for quantifying competitor positioning for frontend visualizations.
"""
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LandscapeItem(BaseModel):
    """
    Quantified competitor positioning for visualization.
    """
    company: str = Field(description="Name of the company.")
    innovation: int = Field(ge=1, le=10, description="Innovation score from 1-10.")
    market_presence: int = Field(ge=1, le=10, description="Market presence/dominance score from 1-10.")


class CompetitiveLandscapeResult(BaseModel):
    """
    Structured output for the competitive landscape chart data.
    """
    landscape: List[LandscapeItem] = Field(description="List of quantified competitors for the map.")


class CompetitiveLandscapeService:
    """
    Service to transform qualitative competitor data into quantitative visualization points.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_landscape_data(
        self, 
        industry: str, 
        competitors_list: List[str]
    ) -> CompetitiveLandscapeResult:
        """
        Generates Innovation vs Market Presence scores for a list of competitors.

        Args:
            industry: The context industry sector.
            competitors_list: List of competitor names to be scored.

        Returns:
            Validated CompetitiveLandscapeResult.
        """
        logger.info("Generating competitive landscape data for %d companies", len(competitors_list))

        system_prompt = (
            "You are a Market Research Specialist and Data Visualization Expert. "
            "Your task is to translate qualitative market knowledge into quantitative scores "
            "for data visualization products. Ensure the relative ordering is logical. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "competitive_landscape_prompt",
            industry=industry,
            competitors_list=", ".join(competitors_list)
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1, # High consistency for scoring
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=CompetitiveLandscapeResult,
            max_retries=3
        )

        logger.info("Competitive landscape data generated successfully.")
        return result

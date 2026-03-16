"""
services/competitor_comparison_service.py
-----------------------------------------
Service for comparing a startup idea with its market rivals to find differentiation.
"""
from __future__ import annotations

from typing import List, Any, Dict
from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ComparisonItem(BaseModel):
    """
    Schema for a single competitor comparison.
    """
    competitor: str = Field(description="Name of the competitor.")
    difference: str = Field(description="Summary of the core differentiation or gap.")


class CompetitorComparisonResult(BaseModel):
    """
    Structured output for the full competitor comparison report.
    """
    comparison: List[ComparisonItem] = Field(description="List of comparisons with specific competitors.")
    strategic_edge: str = Field(description="Overall competitive advantage of the startup idea.")


class CompetitorComparisonService:
    """
    Service to generate strategic comparisons between a startup idea and its competitors.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def compare_with_competitors(
        self, 
        idea_text: str, 
        competitors_data: List[Dict[str, Any]]
    ) -> CompetitorComparisonResult:
        """
        Generates a comparison between the startup idea and a list of competitors.

        Args:
            idea_text: Description of the startup idea.
            competitors_data: A list of dicts containing competitor info (name, products, etc.)

        Returns:
            Validated CompetitorComparisonResult.
        """
        logger.info("Starting competitor comparison for idea...")

        system_prompt = (
            "You are a Lead Strategy Consultant at a top-tier firm. "
            "Your goal is to highlight the competitive differentiation of a new startup idea "
            "against established market players. Focus on feature gaps, market positioning, "
            "and innovation. Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "competitor_comparison_prompt",
            idea_text=idea_text,
            competitors_data=str(competitors_data)
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.3,
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=CompetitorComparisonResult,
            max_retries=3
        )

        logger.info("Competitor comparison completed.")
        return result

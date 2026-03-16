"""
services/competitor_data_service.py
-----------------------------------
Service for collecting granular details for specific market competitors.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CompetitorDataResult(BaseModel):
    """
    Structured output for detailed competitor intelligence.
    """
    name: str = Field(description="The exact name of the competitor.")
    description: str = Field(description="A short, one-sentence description.")
    main_product: str = Field(description="The primary product offering.")
    target_market: str = Field(description="The audience they primarily serve.")
    pricing_model: str = Field(description="Their primary pricing model (e.g., Subscription, Freemium).")


class CompetitorDataService:
    """
    Service to collect granular data for market competitors using AI intelligence.
    Designed for future integration with scraping and APIs.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def get_competitor_details(self, competitor_name: str, industry: str) -> CompetitorDataResult:
        """
        Retrieves detailed intelligence for a specific competitor.

        Args:
            competitor_name: The name of the company or product.
            industry: The context industry.

        Returns:
            Validated CompetitorDataResult.
        """
        logger.info("Collecting data for competitor: %s", competitor_name)

        system_prompt = (
            "You are a Senior Business Analyst specializing in competitive intelligence. "
            "Your task is to provide accurate, factual, and concise data for specified companies. "
            "Focus on the primary product, target audience, and pricing structure. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "competitor_data_prompt",
            competitor_name=competitor_name,
            industry=industry
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.2, # Low temperature for factual consistency
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=CompetitorDataResult,
            max_retries=3
        )

        logger.info("Data collection completed for: %s", result.name)
        return result

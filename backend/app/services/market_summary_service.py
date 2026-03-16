"""
services/market_summary_service.py
---------------------------------
Service for consolidating multi-service market analysis outputs into a concise report.
"""
from __future__ import annotations

from typing import Any, Dict
from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MarketSummaryResult(BaseModel):
    """
    Structured output for the concise market summary.
    """
    summary: str = Field(description="A concise and professional report of the market analysis.")


class MarketSummaryService:
    """
    Generates a high-level executive summary from various market analysis data points.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_summary(self, market_data: Dict[str, Any]) -> MarketSummaryResult:
        """
        Summarizes complex market analysis outputs into a single cohesive report.

        Args:
            market_data: A dictionary containing results from TAM/SAM, Trends, Demand, etc.

        Returns:
            Validated MarketSummaryResult.
        """
        logger.info("Generating executive market summary...")

        system_prompt = (
            "You are a Senior Investment Analyst at a top-tier venture capital firm. "
            "Your task is to synthesize disparate market data into a clear, professional, "
            "and persuasive summary for an investment committee. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "market_summary_prompt",
            market_data=str(market_data)
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.4,
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=MarketSummaryResult,
            max_retries=3
        )

        logger.info("Market summary generated successfully.")
        return result

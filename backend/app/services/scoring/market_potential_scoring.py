"""
services/scoring/market_potential_scoring.py
--------------------------------------------
Specialized scoring module for market potential evaluation.
"""
from __future__ import annotations

from typing import List, Union
from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class MarketPotentialResult(BaseModel):
    """
    Schema for market potential scoring output.
    """
    market_potential_score: int = Field(ge=1, le=10, description="Normalized score from 1-10.")
    reasoning: str = Field(description="Brief justification for the score.")


class MarketPotentialScoring:
    """
    Scoring engine component for market potential dimensions.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def calculate_score(
        self,
        tam: str,
        sam: str,
        growth_rate: str,
        demand_signals: Union[str, List[str]]
    ) -> MarketPotentialResult:
        """
        Calculates a market potential score (1-10) using AI synthesis.
        """
        logger.info("Calculating market potential score...")

        system_prompt = (
            "You are a Quantitative Market Analyst. "
            "Your task is to assign a normalized 1-10 score to market opportunities. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "market_potential_scoring_prompt",
            tam=tam,
            sam=sam,
            growth_rate=growth_rate,
            demand_signals=str(demand_signals)
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1, # High precision
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=MarketPotentialResult,
            max_retries=3
        )

        logger.info("Market potential score calculated: %d", result.market_potential_score)
        return result

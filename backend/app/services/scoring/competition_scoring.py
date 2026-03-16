"""
services/scoring/competition_scoring.py
---------------------------------------
Specialized scoring module for competitive threat evaluation.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CompetitionScoringResult(BaseModel):
    """
    Schema for competition scoring output.
    """
    competition_score: int = Field(ge=1, le=10, description="Normalized score from 1-10. Higher is better (less competition/more moats).")
    reasoning: str = Field(description="Brief justification for the score.")


class CompetitionScoring:
    """
    Scoring engine component for competitive landscape dimensions.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def calculate_score(
        self,
        num_competitors: int,
        competitor_strength: str,
        differentiation_level: str
    ) -> CompetitionScoringResult:
        """
        Calculates a competition score (1-10) using AI synthesis.
        
        Logic:
        - 10 = Blue Ocean, no rivals, high differentiation.
        - 1 = Red Ocean, dominated by giants, low differentiation.
        - Saturated markets naturally pull the score toward the lower end (1-4).
        """
        logger.info("Calculating competition score for %d competitors...", num_competitors)

        system_prompt = (
            "You are a Strategic Competition Analyst. "
            "Your task is to assign a normalized 1-10 score to competitive threats. "
            "A higher score indicates a more favorable (less threatened) position for the startup. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "competition_scoring_prompt",
            num_competitors=num_competitors,
            competitor_strength=competitor_strength,
            differentiation_level=differentiation_level
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1, # High precision for scoring
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=CompetitionScoringResult,
            max_retries=3
        )

        logger.info("Competition score calculated: %d", result.competition_score)
        return result

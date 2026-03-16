"""
services/scoring/scalability_scoring.py
---------------------------------------
Specialized scoring module for evaluating startup scalability.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ScalabilityScoringResult(BaseModel):
    """
    Schema for scalability scoring output.
    """
    scalability_score: int = Field(ge=1, le=10, description="Normalized score from 1-10.")
    reasoning: str = Field(description="Brief justification for the score.")


class ScalabilityScoring:
    """
    Scoring engine component for evaluating exponential growth potential.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def calculate_score(
        self,
        product_scalability: str,
        nature: str,
        global_potential: str
    ) -> ScalabilityScoringResult:
        """
        Calculates a scalability score (1-10) using AI synthesis.
        
        Logic:
        - 10 = Infinite scale, digital, global.
        - 1 = Physical, local, linear cost growth.
        """
        logger.info("Calculating scalability score for nature: %s", nature)

        system_prompt = (
            "You are a Scalability Expert and Venture Architect. "
            "Your task is to assign a normalized 1-10 score to a startup's growth potential. "
            "Prioritize business models with low marginal costs and global reach. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "scalability_scoring_prompt",
            product_scalability=product_scalability,
            nature=nature,
            global_potential=global_potential
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
            model_cls=ScalabilityScoringResult,
            max_retries=3
        )

        logger.info("Scalability score calculated: %d", result.scalability_score)
        return result

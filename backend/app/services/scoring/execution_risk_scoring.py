"""
services/scoring/execution_risk_scoring.py
------------------------------------------
Specialized scoring module for evaluating startup execution hurdles.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionRiskResult(BaseModel):
    """
    Schema for execution risk scoring output.
    """
    execution_risk_score: int = Field(ge=1, le=10, description="Normalized score from 1-10. Higher means MORE risk.")
    reasoning: str = Field(description="Brief justification for the score.")


class ExecutionRiskScoring:
    """
    Scoring engine component for quantifying technical, regulatory, and capital hurdles.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def calculate_score(
        self,
        technical_complexity: str,
        regulatory_barriers: str,
        capital_requirements: str
    ) -> ExecutionRiskResult:
        """
        Calculates an execution risk score (1-10) using AI synthesis.
        
        Logic:
        - 10 = Extreme risk (R&D, Heavy Regulation, High CapEx).
        - 1 = Low risk (Simple Software, No Regulation, Bootstrappable).
        """
        logger.info("Calculating execution risk score...")

        system_prompt = (
            "You are a Quantitative Risk Assessment Expert. "
            "Your task is to assign a normalized 1-10 score to startup execution hurdles. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "execution_risk_scoring_prompt",
            technical_complexity=technical_complexity,
            regulatory_barriers=regulatory_barriers,
            capital_requirements=capital_requirements
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
            model_cls=ExecutionRiskResult,
            max_retries=3
        )

        logger.info("Execution risk score calculated: %d", result.execution_risk_score)
        return result

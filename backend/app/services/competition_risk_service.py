"""
services/competition_risk_service.py
------------------------------------
Service for estimating competitive risk and pressure for a startup idea.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CompetitionRiskResult(BaseModel):
    """
    Structured output for the competition risk assessment.
    """
    competition_level: str = Field(description="Categorical risk level (e.g., High, Moderate).")
    risk_score: int = Field(ge=1, le=10, description="Numerical risk score from 1-10.")
    reasoning: str = Field(description="Detailed explanation of the risk scoring logic.")


class CompetitionRiskService:
    """
    Service to assess market entry risk based on competitive pressure.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def assess_risk(
        self, 
        idea_text: str, 
        industry: str, 
        competitors_context: str,
        differentiation_context: str
    ) -> CompetitionRiskResult:
        """
        Estimates the competitive risk level and provided structured reasoning.

        Args:
            idea_text: description of the startup idea.
            industry: industry classification.
            competitors_context: Summary or list of identified competitors.
            differentiation_context: How the startup claims to differ.

        Returns:
            Validated CompetitionRiskResult.
        """
        logger.info("Assessing competition risk for idea in %s", industry)

        system_prompt = (
            "You are a Senior Risk Analyst and Venture Capital Strategist. "
            "Your task is to objectively quantify the competitive threat facing a new startup. "
            "Be critical, data-driven, and avoid overly optimistic projections. "
            "Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "competition_risk_prompt",
            idea_text=idea_text,
            industry=industry,
            competitors_context=competitors_context,
            differentiation_context=differentiation_context
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.3, # Low temperature for analytical consistency
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=CompetitionRiskResult,
            max_retries=3
        )

        logger.info("Risk assessment completed: Score %d (%s)", result.risk_score, result.competition_level)
        return result

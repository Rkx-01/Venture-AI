"""
services/report_sections/feasibility_section_service.py
------------------------------------------------------
Modular service for generating the feasibility analysis (scoring summary) section of the report.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FeasibilitySectionResult(BaseModel):
    """
    Structured output for the startup feasibility (scoring) summary.
    """
    startup_score_summary: str = Field(description="A professional, investor-friendly explanation of the startup scores.")


class FeasibilitySectionService:
    """
    Specialized service to interpret and explain viability scores.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_feasibility_summary(
        self,
        market_potential_score: int,
        competition_score: int,
        scalability_score: int,
        execution_risk_score: int,
        overall_startup_score: float,
        success_probability: str
    ) -> FeasibilitySectionResult:
        """
        Generates a strategic interpretation of the startup's viability metrics.
        """
        logger.info("Generating feasibility score summary (Overall: %.1f)", overall_startup_score)

        system_prompt = "You are a Senior Venture Capital Partner. Provide a professional interpretation of these startup viability scores."
        
        user_prompt = PromptManager.get_prompt(
            "feasibility_section_prompt",
            market_potential_score=market_potential_score,
            competition_score=competition_score,
            scalability_score=scalability_score,
            execution_risk_score=execution_risk_score,
            overall_startup_score=overall_startup_score,
            success_probability=success_probability
        )

        raw_result = await self.llm.generate_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            response_format_json=True
        )

        import json
        data = json.loads(raw_result)
        return FeasibilitySectionResult(**data)

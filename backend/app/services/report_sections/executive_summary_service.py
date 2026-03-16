"""
services/report_sections/executive_summary_service.py
------------------------------------------------------
Modular service for generating the executive summary section of the report.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutiveSummaryResult(BaseModel):
    """
    Structured output for the executive summary section.
    """
    executive_summary: str = Field(description="A professional and investor-friendly summary of the startup idea.")


class ExecutiveSummaryService:
    """
    Specialized service to generate high-quality executive summaries.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_summary(
        self,
        idea_text: str,
        industry: str,
        target_users: str,
        market_potential_score: int
    ) -> ExecutiveSummaryResult:
        """
        Generates a concise executive summary based on core startup attributes.
        """
        logger.info("Generating executive summary for idea in industry: %s", industry)

        system_prompt = "You are a World-Class Venture Capital Partner. Provide a high-impact, professional executive summary."
        
        user_prompt = PromptManager.get_prompt(
            "executive_summary_prompt",
            idea_text=idea_text,
            industry=industry,
            target_users=target_users,
            market_potential_score=market_potential_score
        )

        raw_result = await self.llm.generate_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
            response_format_json=True
        )

        import json
        data = json.loads(raw_result)
        return ExecutiveSummaryResult(**data)

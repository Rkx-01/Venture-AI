"""
services/report_sections/competitor_section_service.py
------------------------------------------------------
Modular service for generating the competitor landscape section of the report.
"""
from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field
from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CompetitorSectionResult(BaseModel):
    """
    Structured output for the competitor landscape section.
    """
    competitor_landscape: str = Field(description="A strategic analysis of competitors, advantages, and market gaps.")


class CompetitorSectionService:
    """
    Specialized service to generate competitive strategy narratives.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def generate_competitor_section(
        self,
        competitor_list: List[str],
        strengths: List[str],
        weaknesses: List[str],
        competitive_positioning: str
    ) -> CompetitorSectionResult:
        """
        Generates a strategic competitor landscape analysis.
        """
        logger.info("Generating competitor section analysis...")

        system_prompt = "You are a Competitive Strategist and VC Analyst. Provide a high-impact, professional competitor analysis."
        
        user_prompt = PromptManager.get_prompt(
            "competitor_section_prompt",
            competitor_list=", ".join(competitor_list) if competitor_list else "None identified",
            strengths=", ".join(strengths) if strengths else "N/A",
            weaknesses=", ".join(weaknesses) if weaknesses else "N/A",
            competitive_positioning=competitive_positioning
        )

        raw_result = await self.llm.generate_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3,
            response_format_json=True
        )

        import json
        data = json.loads(raw_result)
        return CompetitorSectionResult(**data)

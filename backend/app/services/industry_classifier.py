"""
services/industry_classifier.py
-------------------------------
Service for classifying startup ideas into specific industry sectors and subsectors using AI.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.ai.validators import validate_and_regenerate
from app.utils.logger import get_logger

logger = get_logger(__name__)


class IndustryClassificationResult(BaseModel):
    """
    Structured output for industry classification.
    """
    industry: str = Field(description="The primary industry sector (e.g., FinTech, HealthTech).")
    subsector: str = Field(description="A specific niche or vertical (e.g., Mental Health Apps).")


class IndustryClassifier:
    """
    Service to automatically categorize startup ideas.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def classify_idea(self, idea_text: str) -> IndustryClassificationResult:
        """
        Classifies the provided startup idea text into an industry and subsector.

        Args:
            idea_text: The full description of the startup idea.

        Returns:
            Validated IndustryClassificationResult.
        """
        logger.info("Classifying industry for idea (length: %d)", len(idea_text))

        system_prompt = (
            "You are a professional market research analyst and taxonomist. "
            "Your task is to accurately categorize startup ideas into a canonical industry "
            "and a descriptive subsector. Respond ONLY in valid JSON matching the schema."
        )

        user_prompt = PromptManager.get_prompt(
            "industry_classification_prompt",
            idea_text=idea_text
        )

        async def _call_llm() -> str:
            return await self.llm.generate_chat(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.1,  # Low temperature for deterministic classification
                response_format_json=True
            )

        # Execute with automatic validation and structural retries
        result = await validate_and_regenerate(
            llm_call=_call_llm,
            model_cls=IndustryClassificationResult,
            max_retries=3
        )

        logger.info(
            "Idea classified as %s / %s", 
            result.industry, 
            result.subsector
        )
        return result

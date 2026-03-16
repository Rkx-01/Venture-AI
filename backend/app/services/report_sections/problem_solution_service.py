"""
services/report_sections/problem_solution_service.py
------------------------------------------------------
Modular service for generating the problem-solution analysis section of the report.
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.ai.llm_client import LLMClient
from app.ai.prompt_manager import PromptManager
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ProblemSolutionResult(BaseModel):
    """
    Structured output for the problem-solution analysis section.
    """
    problem_solution_analysis: str = Field(description="A pitch-style explanation of the core problem and solution.")


class ProblemSolutionService:
    """
    Specialized service to generate compelling problem-solution narratives.
    """

    def __init__(self):
        self.llm = LLMClient()

    async def analyze_problem_solution(
        self,
        problem: str,
        solution_type: str,
        target_users: str
    ) -> ProblemSolutionResult:
        """
        Generates a clear and compelling problem-solution analysis.
        """
        logger.info("Generating problem-solution analysis for target users: %s", target_users)

        system_prompt = "You are a Pitch Deck Expert and VC Analyst. Articulate the problem and solution with clarity and impact."
        
        user_prompt = PromptManager.get_prompt(
            "problem_solution_prompt",
            problem=problem,
            solution_type=solution_type,
            target_users=target_users
        )

        raw_result = await self.llm.generate_chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,
            response_format_json=True
        )

        import json
        data = json.loads(raw_result)
        return ProblemSolutionResult(**data)

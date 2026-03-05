"""
ai/llm_client.py
----------------
Core client for communicating with Large Language Models.

Wraps the official OpenAI Async client and provides:
  - Model selection and abstraction.
  - Temperature / token limits.
  - Automatic JSON mode enforcement where supported.
  - Resilient retry logic using Tenacity.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import openai
from openai import AsyncOpenAI
import google.generativeai as genai
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config.settings import get_settings
from app.exceptions import ExternalServiceError
from app.utils.logger import get_logger

logger = get_logger("ai.llm")
settings = get_settings()

# Initialize the async client once
_openai_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    """Returns a singleton instance of the AsyncOpenAI client."""
    global _openai_client
    if _openai_client is None:
        if not settings.OPENAI_API_KEY:
             raise ExternalServiceError("OpenAI API key is missing.", provider="openai")
        _openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())
    return _openai_client


class LLMClient:
    """
    Production wrapper for invoking OpenAI and Gemini chat completions.
    """

    def __init__(self, model: Optional[str] = None, fallback_model: Optional[str] = None):
        if settings.LLM_PROVIDER == "openai":
            self.model = model or "gpt-4o"
            self.fallback_model = fallback_model or "gpt-3.5-turbo"
            self.client = get_openai_client()
        else:
            # Use models confirmed available in user's account
            self.model = model or "gemini-flash-latest"
            self.fallback_model = fallback_model or "gemini-pro-latest"
            genai.configure(api_key=settings.GEMINI_API_KEY.get_secret_value())

    @retry(
        retry=retry_if_exception_type(
            (
                openai.RateLimitError,
                openai.APIConnectionError,
                openai.InternalServerError,
            )
        ),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _generate_with_openai(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        response_format_json: bool = True,
    ) -> str:
        """
        Internal method for OpenAI generation.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        kwargs: Dict[str, Any] = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format_json and "gpt-" in model_name:
            kwargs["response_format"] = {"type": "json_object"}

        logger.info("Calling OpenAI: %s", model_name)

        try:
            response = await self.client.chat.completions.create(**kwargs)  # type: ignore
        except openai.AuthenticationError as e:
            logger.error("OpenAI Authentication failed: %s", str(e))
            raise ExternalServiceError("LLM Provider Authentication Failed.", provider="openai") from e
        except Exception as e:
            logger.error("LLM Provider Error: %s", str(e))
            raise ExternalServiceError("Failed to generate AI response.", provider="openai") from e

        content = response.choices[0].message.content
        if not content:
            raise ExternalServiceError("LLM returned an empty response.", provider="openai")

        return content

    async def _generate_with_gemini(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        response_format_json: bool = True,
    ) -> str:
        """
        Internal method for Gemini generation.
        """
        logger.info("Calling Gemini: %s", model_name)
        
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_prompt
            )
            
            # Use generation_config for temperature and max_tokens
            generation_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json" if response_format_json else "text/plain"
            )

            # Gemini-1.5 supports a single content call
            response = await model.generate_content_async(
                user_prompt,
                generation_config=generation_config
            )
            
            if not response.text:
                raise ExternalServiceError("Gemini returned an empty response.", provider="gemini")
                
            return response.text
        except Exception as e:
            logger.error("Gemini Provider Error (%s): %s", model_name, str(e))
            raise ExternalServiceError(f"Failed to generate Gemini response: {str(e)}", provider="gemini") from e

    async def generate_chat(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1500,
        # Default to True for JSON-heavy backend services
        response_format_json: bool = True,
    ) -> str:
        """
        Sends a fully formatted chat request to the selected LLM provider.
        Now strictly enforces real AI responses or raises exceptions.
        """
        # 1. Try Primary Model
        try:
            if settings.LLM_PROVIDER == "openai":
                return await self._generate_with_openai(
                    self.model, system_prompt, user_prompt, temperature, max_tokens, response_format_json
                )
            else:
                return await self._generate_with_gemini(
                    self.model, system_prompt, user_prompt, temperature, max_tokens, response_format_json
                )
        except Exception as e:
            logger.warning("Primary model (%s) failed: %s. Attempting fallback.", self.model, str(e))
            
            # 2. Handle Fallback Model
            if self.fallback_model and self.model != self.fallback_model:
                try:
                    logger.info("Engaging fallback model: %s", self.fallback_model)
                    if settings.LLM_PROVIDER == "openai":
                        return await self._generate_with_openai(
                            self.fallback_model, system_prompt, user_prompt, temperature, max_tokens, response_format_json
                        )
                    else:
                        return await self._generate_with_gemini(
                            self.fallback_model, system_prompt, user_prompt, temperature, max_tokens, response_format_json
                        )
                except Exception as e2:
                    logger.error("Fallback model (%s) also failed: %s", self.fallback_model, str(e2))
                    raise e2
            
            # Re-raise the primary error if no fallback or fallback failed
            raise e

    async def _get_mock_response(self) -> str:
        """Helper to return a high-fidelity mock response."""
        logger.info("Providing high-fidelity mock response.")
        import asyncio
        import json
        await asyncio.sleep(1.5)
        mock_response = {
            "idea_summary": "An innovative solution focused on resolving existing market inefficiencies through automation and AI-driven insights.",
            "problem_statement": "The target industry currently suffers from high manual overhead and fragmented data processing tools.",
            "target_users": "Enterprise CTOs, small-to-medium business owners, and digital transformation leads.",
            "market_insights": {
                "tam": "$15.4B", 
                "sam": "$2.8B", 
                "som": "$450M", 
                "trends": "Rapid migration to cloud-native architectures and increasing demand for real-time data visualization."
            },
            "competitors": [
                {"name": "LegacyCorp", "description": "Traditional market leader with high pricing.", "strengths": "Brand loyalty", "weaknesses": "Slow innovation"},
                {"name": "FastStack", "description": "Modern startup with nimble features.", "strengths": "Speed", "weaknesses": "Limited enterprise support"}
            ],
            "swot": {
                "strengths": ["Proprietary algorithm", "Low cost structure"], 
                "weaknesses": ["Initial brand awareness", "Small regional team"], 
                "opportunities": ["Unsaturated Asian markets", "Partnership with cloud providers"], 
                "threats": ["Evolving regulatory landscape", "Aggressive VC-backed talent wars"]
            },
            "startup_score": 8.2,
            "investment_recommendation": "Strong Buy - Seed Stage",
            "report": "This venture demonstrates strong unit economics and a clear path to $10M ARR within 24 months, assuming successful execution of the go-to-market strategy detailed in the findings."
        }
        return json.dumps(mock_response)

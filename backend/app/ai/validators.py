"""
ai/validators.py
----------------
Utilities for structural validation and automatic regeneration of LLM outputs.
"""
from __future__ import annotations

from typing import Awaitable, Callable, Type, TypeVar

from pydantic import BaseModel

from app.ai.response_parser import ResponseParser
from app.exceptions import ExternalServiceError
from app.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


async def validate_and_regenerate(
    llm_call: Callable[[], Awaitable[str]],
    model_cls: Type[T],
    max_retries: int = 3,
) -> T:
    """
    Executes an LLM call and validates the raw text against a target Pydantic schema.
    If fields are missing or invalid, it triggers automatic regeneration up to `max_retries`.
    
    Args:
        llm_call: An async zero-argument callable that triggers the `generate_chat` request.
        model_cls: The expected Pydantic schema class.
        max_retries: Total allowed attempts if parsing fails.
        
    Returns:
        The validated Pydantic object.
        
    Raises:
        ExternalServiceError: If the maximum retry budget is exhausted and parsing still fails.
    """
    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            # Trigger the LLM generation
            raw_response = await llm_call()

            # The parser evaluates JSON integrity and Pydantic structural integrity.
            # If a field like 'revenue_model' is missing, parse_as throws an ExternalServiceError.
            return ResponseParser.parse_as(model_cls, raw_response)

        except ExternalServiceError as e:
            last_exception = e
            logger.warning(
                "LLM Data Validation Error. Attempt %d/%d failed: %s",
                attempt,
                max_retries,
                str(e),
                extra={"attempt": attempt, "error_details": str(e)},
            )
            if attempt == max_retries:
                logger.error("Max schema regeneration retries exhausted.")
                raise e

    # Fallback to satisfy typing, though the loop will always raise or return.
    raise last_exception or ExternalServiceError("Validation retries exhausted unexpectedly.")

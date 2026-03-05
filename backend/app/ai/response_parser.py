"""
ai/response_parser.py
---------------------
Parses and validates unstructured text from LLMs into structured Pydantic models.
"""
from __future__ import annotations

import json
import re
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

from app.exceptions import ExternalServiceError
from app.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


class ResponseParser:
    """
    Utility class to safely extract and validate JSON from raw LLM text outputs.
    """

    @staticmethod
    def extract_json(raw_text: str) -> str:
        """
        Attempts to find a JSON block in the raw text.
        Useful when the LLM wraps the JSON in markdown code blocks like ```json ... ```.
        """
        # Fast path: if the text looks like an object, just return it
        raw_text = raw_text.strip()
        if raw_text.startswith("{") and raw_text.endswith("}"):
            return raw_text

        if raw_text.startswith("[") and raw_text.endswith("]"):
            return raw_text

        # Regex search for ```json ... ``` blocks
        json_pattern = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
        match = json_pattern.search(raw_text)
        if match:
            return match.group(1).strip()
            
        # Fallback: hope the raw text is actually valid JSON despite missing brackets at ends
        return raw_text

    @classmethod
    def parse_as(cls, model: Type[T], raw_text: str) -> T:
        """
        Extracts JSON from the LLM output and validates it against a Pydantic model.
        
        Args:
            model: The Pydantic model class to validate against.
            raw_text: The complete string response from the LLM.
            
        Raises:
            ExternalServiceError: If parsing fails or the schema is invalid.
        """
        extracted = cls.extract_json(raw_text)
        
        try:
            data_dict = json.loads(extracted)
        except json.JSONDecodeError as e:
            logger.error("Failed to decode JSON from LLM: %s | Raw: %s", str(e), raw_text[:200])
            raise ExternalServiceError(
                "LLM returned invalid JSON format.", provider="llm_parser"
            ) from e

        try:
            return model.model_validate(data_dict)
        except ValidationError as e:
            logger.error("LLM JSON failed schema validation: %s", str(e))
            raise ExternalServiceError(
                "LLM output did not match the required schema.", provider="llm_parser"
            ) from e

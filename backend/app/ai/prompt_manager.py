"""
ai/prompt_manager.py
--------------------
Centralized repository for all LLM prompt templates.

Templates are stored as .txt files in the ai/prompts/ directory.
Variables are injected using the {{variable_name}} syntax.
Versioning is supported via filename conventions (e.g. prompt_v2.txt).
"""
from __future__ import annotations
from typing import Optional

from pathlib import Path
from typing import Any

from app.exceptions import InternalError
from app.utils.logger import get_logger

logger = get_logger(__name__)

PROMPTS_DIR = Path(__file__).parent / "prompts"


class PromptManager:
    """
    Manages loading and rendering of file-based prompt templates.
    """

    # In-memory cache to avoid disk I/O on every AI call in production
    _cache: dict[str, str] = {}

    @classmethod
    def get_prompt(cls, template_name: str, version: Optional[str] = None, **kwargs: Any) -> str:
        """
        Loads a prompt template from disk and injects the provided variables.
        
        Args:
            template_name: The base name of the prompt (e.g. "startup_idea_analysis_prompt")
            version: Optional version tag (e.g. "v2"). If provided, loads "name_v2.txt".
            **kwargs: Variables to inject into the template placeholders (e.g. {{startup_idea}}).
            
        Returns:
            The fully rendered prompt string.
            
        Raises:
            InternalError: If the template file cannot be found on disk.
            KeyError: If a required {{variable}} is missing in the kwargs.
        """
        # 1. Resolve filename
        filename = template_name
        if version:
            filename = f"{template_name}_{version}"
        if not filename.endswith(".txt"):
            filename += ".txt"

        # 2. Check cache or load from disk
        prompt_text = cls._cache.get(filename)
        if prompt_text is None:
            filepath = PROMPTS_DIR / filename
            if not filepath.exists():
                logger.error("Prompt template not found: %s", filepath)
                raise InternalError(
                    f"Prompt template '{filename}' is missing from the system.",
                    provider="prompt_manager"
                )
            
            prompt_text = filepath.read_text(encoding="utf-8")
            # Cache in production for speed
            cls._cache[filename] = prompt_text

        # 3. Inject variables manually to support the {{variable}} syntax
        # We don't use .format() because LLMs use {} for JSON natively,
        # which clashes with standard Python string formatting.
        rendered = prompt_text
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"  # renders as {{key}}
            rendered = rendered.replace(placeholder, str(value))

        # 4. Safety check: ensure no unresolved variables remain
        if "{{" in rendered and "}}" in rendered:
            # Example extraction: "... {{missing_var}} ..." -> "missing_var"
            missing = rendered.split("{{", 1)[1].split("}}", 1)[0]
            raise KeyError(
                f"Missing required variable '{{{{{missing}}}}}' "
                f"for prompt template '{filename}'."
            )

        return rendered

    @classmethod
    def clear_cache(cls) -> None:
        """Clears the prompt template cache (useful for tests or dynamic reloads)."""
        cls._cache.clear()

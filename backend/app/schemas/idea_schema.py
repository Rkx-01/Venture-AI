"""
schemas/idea_schema.py
----------------------
Pydantic schemas for the startup idea analysis endpoint.

Covers:
  - AnalyzeIdeaRequest   — validated + sanitized input from the client
  - AnalyzeIdeaResponse  — structured response returned to the client

Validation rules enforced at the schema layer (before any service is called):

  idea_text
    - Required, non-empty string
    - Minimum 30 characters  (ensures a meaningful idea description)
    - Maximum 2000 characters (prevents prompt injection padding attacks)
    - Leading/trailing whitespace stripped automatically
    - Consecutive whitespace collapsed to a single space
    - Rejects strings that are only whitespace after strip

  industry
    - Optional with a default of "General"
    - Maximum 100 characters
    - Must match an allowed value from the VALID_INDUSTRIES set
    - Normalised to Title Case on input (e.g. "fintech" → "FinTech")

  target_market
    - Optional free-text field
    - Maximum 300 characters if provided

All validation errors are handled automatically by FastAPI and formatted by
the global validation_exception_handler in exceptions/handlers.py.
"""

from __future__ import annotations
from typing import Optional

import re
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Allowed industry values
# ---------------------------------------------------------------------------

VALID_INDUSTRIES: frozenset[str] = frozenset({
    "FinTech",
    "HealthTech",
    "EdTech",
    "AgriTech",
    "LegalTech",
    "CleanTech",
    "PropTech",
    "InsurTech",
    "RetailTech",
    "HRTech",
    "Cybersecurity",
    "AI / ML",
    "SaaS",
    "Marketplace",
    "E-commerce",
    "Gaming",
    "Media",
    "Logistics",
    "SpaceTech",
    "BioTech",
    "General",
})

# Pre-computed lowercase → canonical map for case-insensitive matching
_INDUSTRY_MAP: dict[str, str] = {v.lower(): v for v in VALID_INDUSTRIES}


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------


class AnalyzeIdeaRequest(BaseModel):
    """
    Request body for POST /api/v1/analyze.

    Validates, sanitizes, and normalises user input before it reaches
    service-layer code or an LLM prompt.
    """

    idea_text: str = Field(
        ...,
        max_length=2000,
        description="Full description of the startup idea.",
        examples=["AI powered mental health app for college students"],
    )
    industry: str = Field(
        default="General",
        max_length=100,
        description=(
            f"Industry vertical. One of: {', '.join(sorted(VALID_INDUSTRIES))}. "
            "Defaults to 'General'."
        ),
        examples=["HealthTech"],
    )
    target_market: Optional[str] = Field(
        default=None,
        max_length=300,
        description="Optional description of the intended target market.",
        examples=["College students aged 18–24 in the US"],
    )

    # ------------------------------------------------------------------
    # Field validators (run before model_validator)
    # ------------------------------------------------------------------

    @field_validator("idea_text", mode="before")
    @classmethod
    def sanitize_idea_text(cls, v: str) -> str:
        """
        1. Strip leading/trailing whitespace.
        2. Collapse runs of internal whitespace to a single space.
        3. Reject strings that are entirely whitespace.
        """
        if not isinstance(v, str):
            raise ValueError("idea_text must be a string.")

        v = v.strip()
        if not v:
            raise ValueError("idea_text must not be empty or contain only whitespace.")
        
        # Collapse consecutive whitespace
        v = re.sub(r"\s+", " ", v)
        return v

    @field_validator("industry", mode="before")
    @classmethod
    def normalise_industry(cls, v: str) -> str:
        """
        Case-insensitive match against VALID_INDUSTRIES.
        Returns the canonical casing (e.g. 'fintech' → 'FinTech').
        """
        if not isinstance(v, str):
            raise ValueError("industry must be a string.")

        normalised = _INDUSTRY_MAP.get(v.strip().lower())
        if normalised is None:
            valid_list = ", ".join(sorted(VALID_INDUSTRIES))
            raise ValueError(
                f"'{v}' is not a recognised industry. "
                f"Valid options are: {valid_list}."
            )
        return normalised

    @field_validator("target_market", mode="before")
    @classmethod
    def sanitize_target_market(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(v)).strip()
        return v if v else None

    # ------------------------------------------------------------------
    # Cross-field validation
    # ------------------------------------------------------------------

    model_config = {
        "json_schema_extra": {
            "example": {
                "idea_text": "AI powered mental health app for college students",
                "industry": "HealthTech",
                "target_market": "College students aged 18–24 in the US",
            }
        }
    }


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class AnalysisStatus(str):
    """Possible states of an analysis job."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalyzeIdeaResponse(BaseModel):
    """
    Immediate response after submitting an idea for analysis.
    The full report is fetched separately once status = 'completed'.
    """

    analysis_id: uuid.UUID = Field(
        description="Unique ID to poll for analysis results."
    )
    status: Literal["pending", "processing", "completed", "failed"] = Field(
        default="pending",
        description="Current state of the analysis job.",
    )
    message: str = Field(
        default="Your startup idea has been queued for analysis.",
        description="Human-readable status message.",
    )
    submitted_at: datetime = Field(
        description="UTC timestamp of when the idea was received.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "analysis_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "status": "pending",
                "message": "Your startup idea has been queued for analysis.",
                "submitted_at": "2026-03-05T10:00:00Z",
            }
        }
    }


class IdeaResponse(BaseModel):
    """
    Schema for representing a fetched Idea in the collection.
    """
    id: uuid.UUID
    idea_text: str
    industry: str

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "idea_text": "AI productivity assistant for remote teams",
            }
        }
    }

IdeaRequest = AnalyzeIdeaRequest

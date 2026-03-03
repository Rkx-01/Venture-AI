"""
models/startup_score.py
-----------------------
ORM model for storing AI-generated startup viability scores and success probabilities.
"""
from __future__ import annotations

import uuid
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.startup_idea import StartupIdea


class StartupScore(UUIDMixin, TimestampMixin, Base):
    """
    Represents the final viability synthesis and scoring for a startup idea.
    """

    __tablename__ = "startup_scores"

    startup_idea_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("startup_ideas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the scored startup idea.",
    )

    market_potential_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Market potential score (1-10).",
    )
    competition_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Competition score (1-10).",
    )
    scalability_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Scalability score (1-10).",
    )
    execution_risk_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Execution risk score (1-10).",
    )
    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Weighted composite score (1.0-10.0).",
    )
    success_probability: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Estimated success probability percentage (e.g., '75%').",
    )

    # Relationships
    startup_idea: Mapped["StartupIdea"] = relationship(
        "StartupIdea", 
        back_populates="startup_scores"
    )

    def __repr__(self) -> str:
        return (
            f"StartupScore(id={self.id!r}, startup_idea_id={self.startup_idea_id!r}, "
            f"overall={self.overall_score!r}, prob={self.success_probability!r})"
        )

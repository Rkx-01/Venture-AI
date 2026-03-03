"""
models/market_analysis.py
-------------------------
ORM model for storing AI-generated market analysis results.
"""
from __future__ import annotations

import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.startup_idea import StartupIdea


class MarketAnalysis(UUIDMixin, TimestampMixin, Base):
    """
    Represents an AI-generated market evaluation for a specific startup idea.
    """

    __tablename__ = "market_analyses"

    startup_idea_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("startup_ideas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the analyzed startup idea.",
    )

    tam: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Total Addressable Market estimate.",
    )
    sam: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Serviceable Available Market estimate.",
    )
    som: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Serviceable Obtainable Market estimate.",
    )
    industry_growth_rate: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Estimated industry CAGR.",
    )
    market_opportunity_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Overall opportunity score (1-10).",
    )

    # Relationships
    startup_idea: Mapped["StartupIdea"] = relationship(
        "StartupIdea", 
        back_populates="market_analyses"
    )

    def __repr__(self) -> str:
        return (
            f"MarketAnalysis(id={self.id!r}, startup_idea_id={self.startup_idea_id!r}, "
            f"score={self.market_opportunity_score!r})"
        )

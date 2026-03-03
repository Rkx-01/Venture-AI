"""
models/competitor.py
--------------------
ORM model for storing identified competitors for startup ideas.
"""
from __future__ import annotations
from typing import List

import uuid
from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.startup_idea import StartupIdea


class Competitor(UUIDMixin, TimestampMixin, Base):
    """
    Represents a market competitor identified for a specific startup idea.
    """

    __tablename__ = "competitors"

    startup_idea_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("startup_ideas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Reference to the analyzed startup idea.",
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Name of the competitor company or product.",
    )
    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True,
        comment="Brief description of the competitor.",
    )
    target_market: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="Primary audience or market segment.",
    )
    pricing_model: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        comment="Known or estimated pricing strategy.",
    )
    
    # Store list of strengths and weaknesses as JSONB for flexibility and performance
    strengths: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=True,
        comment="JSON array of competitor strengths.",
    )
    weaknesses: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=True,
        comment="JSON array of competitor weaknesses.",
    )

    # Relationships
    startup_idea: Mapped["StartupIdea"] = relationship(
        "StartupIdea", 
        back_populates="competitors"
    )

    def __repr__(self) -> str:
        return f"Competitor(id={self.id!r}, name={self.name!r}, idea_id={self.startup_idea_id!r})"

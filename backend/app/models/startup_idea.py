"""
models/startup_idea.py
----------------------
ORM model for a startup idea submitted by a user for AI analysis.
"""
from __future__ import annotations
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.competitor import Competitor
    from app.models.market_analysis import MarketAnalysis
    from app.models.startup_score import StartupScore


class StartupIdea(UUIDMixin, TimestampMixin, Base):
    """
    Represents a startup idea submitted for AI-powered analysis.

    Columns
    -------
    id          UUID primary key (auto-generated).
    idea_text   The raw startup idea description provided by the user.
    industry    Industry vertical, e.g. "FinTech", "HealthTech".
    created_at  Server-side UTC timestamp set on INSERT.
    updated_at  Server-side UTC timestamp updated on every UPDATE.
    """

    __tablename__ = "startup_ideas"

    idea_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Full description of the startup idea as entered by the user.",
    )
    industry: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Industry vertical, e.g. FinTech, HealthTech, EdTech.",
    )
    target_users: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="AI-extracted target demographic.",
    )
    problem: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="AI-extracted core problem.",
    )
    solution_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="AI-extracted format of the solution.",
    )
    revenue_model: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="AI-extracted money making strategy.",
    )
    embedding: Mapped[Optional[list[float]]] = mapped_column(
        Vector(1536),  # OpenAI text-embedding-3-small dimension
        nullable=True,
        comment="Vector embedding of the idea_text for similarity search.",
    )

    # Relationships
    market_analyses: Mapped[list["MarketAnalysis"]] = relationship(
        "MarketAnalysis", 
        back_populates="startup_idea", 
        cascade="all, delete-orphan"
    )

    competitors: Mapped[list["Competitor"]] = relationship(
        "Competitor", 
        back_populates="startup_idea", 
        cascade="all, delete-orphan"
    )

    startup_scores: Mapped[list["StartupScore"]] = relationship(
        "StartupScore", 
        back_populates="startup_idea", 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"StartupIdea(id={self.id!r}, industry={self.industry!r}, "
            f"created_at={self.created_at!r})"
        )

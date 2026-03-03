"""
database/base.py
----------------
Declarative base and shared column mixins for all ORM models.

All models must import Base from here (not from SQLAlchemy directly)
so that Alembic's autogenerate can discover them via metadata.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.x declarative base.

    All ORM models in app/models/ must inherit from this class.
    Alembic reads Base.metadata to autogenerate migrations.
    """
    pass


# ---------------------------------------------------------------------------
# Reusable mixins — compose into models as needed
# ---------------------------------------------------------------------------

class UUIDMixin:
    """Adds a UUID primary key column."""
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )


class TimestampMixin:
    """Adds server-side created_at and updated_at timestamp columns."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

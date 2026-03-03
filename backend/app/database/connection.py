"""
database/connection.py
----------------------
Async database engine, session factory, and FastAPI dependency.

Design decisions:
- Uses SQLAlchemy 2.x async engine (asyncpg driver).
- Session is created per-request via FastAPI's dependency injection —
  never shared across requests.
- engine is a module-level singleton; recreating it on every request
  is expensive and defeats connection pooling.
"""
from __future__ import annotations
from typing import Optional

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import get_settings

settings = get_settings()

# ---------------------------------------------------------------------------
# Engine & Session Factory — only initialized if DATABASE_URL is present
# ---------------------------------------------------------------------------
engine = None
AsyncSessionLocal = None

if settings.DATABASE_URL:
    engine = create_async_engine(
        settings.DATABASE_URL,
        # Echo SQL only in development to avoid leaking queries to prod logs
        echo=settings.is_debug,
        # Pool tuning — sensible production defaults
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,   # Detect stale connections before checkout
        pool_recycle=3600,    # Recycle connections after 1 hour
    )

    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Keep model attributes accessible after commit
        autoflush=False,
        autocommit=False,
    )



# ---------------------------------------------------------------------------
# FastAPI dependency — yields one session per request, always closed on exit
# ---------------------------------------------------------------------------
async def get_db() -> AsyncGenerator[Optional[AsyncSession], None]:
    """
    Async database session dependency for FastAPI route handlers.
    """
    if settings.USE_MOCK_DB or AsyncSessionLocal is None:
        yield None
        return

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

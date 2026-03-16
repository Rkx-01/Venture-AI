"""
alembic/env.py
--------------
Alembic environment configuration for async SQLAlchemy.

Key responsibilities:
1. Load settings from app.config — keeps DB URL out of alembic.ini.
2. Import ALL models via app.models so Base.metadata includes their tables.
3. Run migrations asynchronously using asyncio.run() + run_sync().
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import get_settings

# Import Base AND all models so their tables register on Base.metadata
from app.database.base import Base
import app.models  # noqa: F401 — side-effect import to register all models

# ---------------------------------------------------------------------------
# Alembic Config object — provides access to values in alembic.ini
# ---------------------------------------------------------------------------
config = context.config
settings = get_settings()

# Inject the real DB URL at runtime (keeps secrets out of alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Setup Python logging from alembic.ini [loggers] section
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic which metadata to compare against for autogenerate
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Offline mode — generates SQL without a live DB connection
# ---------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    Useful for generating SQL scripts to review before applying.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,         # Detect column type changes
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online mode — applies migrations against the live database
# ---------------------------------------------------------------------------
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode using an async engine.
    Uses run_sync() to bridge the async engine with Alembic's sync API.
    """
    connectable = create_async_engine(settings.DATABASE_URL, echo=False)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

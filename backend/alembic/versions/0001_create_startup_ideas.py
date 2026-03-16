"""
alembic/versions/0001_create_startup_ideas.py
----------------------------------------------
Initial migration: creates the startup_ideas table.

Generated manually as a baseline. After this, use:
    alembic revision --autogenerate -m "your description"
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "startup_ideas",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("idea_text", sa.Text(), nullable=False),
        sa.Column("industry", sa.String(100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    # Index on industry for filtered queries
    op.create_index("ix_startup_ideas_id", "startup_ideas", ["id"])
    op.create_index("ix_startup_ideas_industry", "startup_ideas", ["industry"])


def downgrade() -> None:
    op.drop_index("ix_startup_ideas_industry", table_name="startup_ideas")
    op.drop_index("ix_startup_ideas_id", table_name="startup_ideas")
    op.drop_table("startup_ideas")

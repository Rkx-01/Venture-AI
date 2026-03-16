"""Initial migration — placeholder template.

Revision ID: %(rev)s
Revises: %(down_rev)s
Create Date: %(create_date)s
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = %(repr)s
down_revision: Union[str, None] = %(down_rev)s
branch_labels: Union[str, Sequence[str], None] = %(branch_labels)s
depends_on: Union[str, Sequence[str], None] = %(depends_on)s


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

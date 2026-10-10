"""create initial schema

Revision ID: b4e5b39cfe88
Revises: 
Create Date: 2026-10-10 08:27:39.026872
"""

from typing import Sequence, Union

from alembic import op

from app.database.base import Base
import app.database.models  # noqa: F401


revision: str = 'b4e5b39cfe88'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())

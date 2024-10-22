"""Add major to Student

Revision ID: 674855d239d3
Revises: d8566d5294d9
Create Date: 2024-10-11 12:35:04.942127

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "674855d239d3"
down_revision: Union[str, None] = "d8566d5294d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("students", sa.Column("major", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("students", "major")

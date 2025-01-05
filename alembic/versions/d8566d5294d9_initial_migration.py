"""Initial migration

Revision ID: d8566d5294d9
Revises: 9d8a576bd49d
Create Date: 2024-10-11 11:31:42.952093

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "d8566d5294d9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("age", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="students_pkey"),
    )
    op.create_index("ix_students_name", "students", ["name"], unique=False)
    op.create_index("ix_students_id", "students", ["id"], unique=False)
    op.create_index("ix_students_email", "students", ["email"], unique=True)
    op.create_unique_constraint(None, "students", ["email"])


def downgrade() -> None:
    op.drop_index("ix_students_email", table_name="students")
    op.drop_index("ix_students_id", table_name="students")
    op.drop_index("ix_students_name", table_name="students")
    op.drop_constraint(None, "students", type_="unique")
    op.drop_table("students")

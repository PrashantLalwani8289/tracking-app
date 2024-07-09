"""empty message

Revision ID: 265bd9c5a72c
Revises: 
Create Date: 2024-07-09 13:25:04.931703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '265bd9c5a72c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column(
            "account_type",
            sa.Enum("user", "admin", name="account_type_enum"),
            nullable=False,
        ),
        sa.Column("created_ts", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column(
            "updated_ts",
            sa.DateTime(),
            nullable=True,
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    pass

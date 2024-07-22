"""create tables

Revision ID: ff14ed6f2d98
Revises: 
Create Date: 2024-07-22 10:32:34.658055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff14ed6f2d98'
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
        sa.Column("is_active", sa.Boolean, default=False, nullable=False),
        sa.Column("created_ts", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
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
    
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('token', sa.Text),
        sa.Column('created_ts', sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True),
                  default=sa.func.now(), onupdate=sa.func.now()),
    )
 


def downgrade() -> None:
    pass

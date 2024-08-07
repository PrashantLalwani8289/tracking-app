"""creating tables

Revision ID: c131580e6711
Revises: 
Create Date: 2024-08-07 17:35:11.837959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c131580e6711'
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
    # op.create_index(op.f('ix_user_sessions_id'), 'user_sessions', ['id'], unique=False)
    
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('descryption', sa.Text(), nullable=False),
        sa.Column('category', sa.Enum('Technology', 'Health', 'Travel', 'Education', 'Finance', name='category_enum'), nullable=False),
        sa.Column('mainImage', sa.String(), nullable=True),
        sa.Column('approved', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_ts', sa.DateTime(timezone=True), nullable=True, default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True), nullable=True, default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade() -> None:
    pass

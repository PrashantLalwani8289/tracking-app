"""add likes table

Revision ID: 61ee5aad7fe8
Revises: 43d3c133fa9e
Create Date: 2024-09-06 17:51:39.572788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61ee5aad7fe8'
down_revision: Union[str, None] = '43d3c133fa9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('likes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('blog_id', sa.Integer(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_likes_id'), 'likes', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_likes_id'), table_name='likes')
    op.drop_table('likes')

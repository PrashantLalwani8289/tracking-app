"""add blog_id column

Revision ID: 43d3c133fa9e
Revises: 03bc8ff9b51c
Create Date: 2024-09-06 15:26:45.154729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43d3c133fa9e'
down_revision: Union[str, None] = '03bc8ff9b51c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'comment',
        sa.Column('blog_id', sa.Integer, sa.ForeignKey('blogs.id', ondelete="CASCADE"), nullable=False),
    )


def downgrade() -> None:
    pass

"""remove blog_id column

Revision ID: 03bc8ff9b51c
Revises: 01f09d3eb7df
Create Date: 2024-09-06 15:21:29.552286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03bc8ff9b51c'
down_revision: Union[str, None] = '01f09d3eb7df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Remove the blog_id column from the comment table
    op.drop_column('comment', 'blog_id')

def downgrade():
    # Add the blog_id column back if necessary
    op.add_column(
        'comment',
        sa.Column('blog_id', sa.Integer, sa.ForeignKey('blogs.id', ondelete="CASCADE"), nullable=False),
    )
"""create comment table

Revision ID: 01f09d3eb7df
Revises: 4b972b2e5e37
Create Date: 2024-09-06 15:13:40.153339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01f09d3eb7df'
down_revision: Union[str, None] = '4b972b2e5e37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create the comment table
    op.create_table(
        'comment',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('created_ts', sa.DateTime(timezone=True), default=sa.func.now(), nullable=False),
        sa.Column('updated_ts', sa.DateTime(timezone=True), default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.Column('blog_id', sa.Integer, sa.ForeignKey('blogs.id', ondelete="CASCADE"), nullable=False),
        sa.Column('parent_id', sa.Integer, default=None),
    )

def downgrade():
    # Drop the comment table
    op.drop_table('comment')
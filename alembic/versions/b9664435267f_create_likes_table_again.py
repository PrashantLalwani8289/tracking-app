"""create likes table again

Revision ID: b9664435267f
Revises: 14be405dcad3
Create Date: 2024-09-06 18:12:15.758158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9664435267f'
down_revision: Union[str, None] = '14be405dcad3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
        'like',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete="CASCADE"), nullable=False),
        sa.Column('created_ts', sa.DateTime(timezone=True), default=sa.func.now(), nullable=False),
        sa.Column('blog_id', sa.Integer, sa.ForeignKey('blogs.id', ondelete="CASCADE"), nullable=False),
    )


def downgrade() -> None:
    pass

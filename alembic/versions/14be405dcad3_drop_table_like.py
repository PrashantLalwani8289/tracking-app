"""drop table like

Revision ID: 14be405dcad3
Revises: 61ee5aad7fe8
Create Date: 2024-09-06 18:10:23.071878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14be405dcad3'
down_revision: Union[str, None] = '61ee5aad7fe8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f('ix_likes_id'), table_name='likes')
    op.drop_table('likes')


def downgrade() -> None:
    pass

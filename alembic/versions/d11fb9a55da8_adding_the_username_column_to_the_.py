"""adding the username column to the comment table

Revision ID: d11fb9a55da8
Revises: 4517777a1227
Create Date: 2024-09-10 12:02:14.715372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd11fb9a55da8'
down_revision: Union[str, None] = '4517777a1227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('comment', sa.Column('user_name', sa.String(), nullable=False))


def downgrade() -> None:
    pass

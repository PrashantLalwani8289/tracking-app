"""create a table for test

Revision ID: 041b2d4df04b
Revises: 03d78d2f7ab9
Create Date: 2024-09-10 11:14:12.024597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '041b2d4df04b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'testing',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    pass

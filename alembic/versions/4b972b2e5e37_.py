"""empty message

Revision ID: 4b972b2e5e37
Revises: f27b2485ea10
Create Date: 2024-08-26 12:58:41.320975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b972b2e5e37'
down_revision: Union[str, None] = 'f27b2485ea10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'contact_form',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('subject', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=False),
    )


def downgrade() -> None:
    pass

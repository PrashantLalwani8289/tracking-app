"""Add destination_place to blogs

Revision ID: f006f75acd0f
Revises: 17d677aea279
Create Date: 2024-11-13 15:35:53.852868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f006f75acd0f'
down_revision: Union[str, None] = '17d677aea279'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add the new column `destination_place` to the `blogs` table
    op.add_column('blogs', sa.Column('destination_place', sa.Text(), nullable=True,default=None))


def downgrade():
    # Remove the `destination_place` column if rolling back the migration
    op.drop_column('blogs', 'destination_place')
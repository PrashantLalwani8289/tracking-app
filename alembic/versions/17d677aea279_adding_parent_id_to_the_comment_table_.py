"""adding parent_id to the comment table again

Revision ID: 17d677aea279
Revises: b78211d8c940
Create Date: 2024-09-10 12:09:11.770347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17d677aea279'
down_revision: Union[str, None] = 'b78211d8c940'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('comment', sa.Column('parent_id', sa.Integer(), nullable=True))



def downgrade() -> None:
    pass

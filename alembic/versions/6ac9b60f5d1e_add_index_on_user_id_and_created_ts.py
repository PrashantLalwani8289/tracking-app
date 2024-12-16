"""Add index on user_id and created_ts

Revision ID: 6ac9b60f5d1e
Revises: adab78eea095
Create Date: 2024-12-16 11:17:33.654888

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6ac9b60f5d1e"
down_revision: Union[str, None] = "adab78eea095"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("idx_user_created_ts", "blogs", ["user_id", "created_ts"])


def downgrade() -> None:
    op.drop_index("idx_user_created_ts", table_name="blogs")

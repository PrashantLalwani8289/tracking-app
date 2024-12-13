"""create tables

Revision ID: adab78eea095
Revises: 
Create Date: 2024-12-03 16:58:11.198134

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision: str = "adab78eea095"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), unique=True, nullable=True),
        sa.Column(
            "account_type",
            sa.Enum("user", "admin", name="account_type"),
            nullable=False,
        ),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_ts", sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column(
            "updated_ts",
            sa.DateTime(timezone=True),
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # Create user_sessions table
    op.create_table(
        "user_sessions",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("token", sa.Text, nullable=True),
        sa.Column("created_ts", sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column(
            "updated_ts",
            sa.DateTime(timezone=True),
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # Create subscribers table
    op.create_table(
        "subscribers",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
    )

    # Create contact_form table
    op.create_table(
        "contact_form",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("subject", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=False),
    )

    # Create blogs table
    op.create_table(
        "blogs",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("destination_place", sa.Text, nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("introduction", sa.Text(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "Beach",
                "Camping",
                "Hiking",
                "Desert",
                "Forest",
                "LongDrives",
                "FamilyTrips",
                name="blog_category",
            ),
            nullable=False,
        ),
        sa.Column("mainImage", sa.String(), nullable=True),
        sa.Column("photos", ARRAY(sa.String), nullable=False),
        sa.Column("tips", sa.String(), nullable=True),
        sa.Column("adventure", sa.String(), nullable=False),
        sa.Column("accomodationReview", sa.String(), nullable=True),
        sa.Column("destinationGuides", sa.String(), nullable=True),
        sa.Column("customerReview", sa.String(), nullable=True),
        sa.Column("travelChallenges", sa.String(), nullable=True),
        sa.Column("conclusion", sa.String(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("approved", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_ts", sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column(
            "updated_ts",
            sa.DateTime(timezone=True),
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    # Create comment table
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("user_name", sa.String(), nullable=False),
        sa.Column("blog_id", sa.Integer, sa.ForeignKey("blogs.id")),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_ts", sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column(
            "updated_ts",
            sa.DateTime(timezone=True),
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.Column("parent_id", sa.Integer, nullable=True),
    )

    # Create like table
    op.create_table(
        "like",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("blog_id", sa.Integer, nullable=False),
        sa.Column("created_ts", sa.DateTime(timezone=True), default=sa.func.now()),
    )


def downgrade():
    op.drop_table("like")
    op.drop_table("comment")
    op.drop_table("blogs")
    op.drop_table("contact_form")
    op.drop_table("subscribers")
    op.drop_table("user_sessions")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS account_type")
    op.execute("DROP TYPE IF EXISTS blog_category")

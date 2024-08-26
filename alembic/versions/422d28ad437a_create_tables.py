"""create tables

Revision ID: 422d28ad437a
Revises: 
Create Date: 2024-08-10 18:35:31.086983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '422d28ad437a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column(
            "account_type",
            sa.Enum("user", "admin", name="account_type_enum"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean, default=False, nullable=False),
        sa.Column("created_ts", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "updated_ts",
            sa.DateTime(),
            nullable=True,
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('token', sa.Text),
        sa.Column('created_ts', sa.DateTime(timezone=True), default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True),
                  default=sa.func.now(), onupdate=sa.func.now()),
    )
    # op.create_index(op.f('ix_user_sessions_id'), 'user_sessions', ['id'], unique=False)
    
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('introduction', sa.Text(), nullable=False),
        sa.Column('category',sa.Enum('Technology', 'Health', 'Travel', 'Education', 'Finance', 'other', name='category_enum') , nullable=False),
        sa.Column('mainImage', sa.String(), nullable=True),
        sa.Column('photos', postgresql.ARRAY(sa.String), nullable=False),
        sa.Column('tips', sa.String(), nullable=True),
        sa.Column('adventure', sa.String(), nullable=False),
        sa.Column('accomodationReview', sa.String(), nullable=True),
        sa.Column('destinationGuides', sa.String(), nullable=True),
        sa.Column('customerReview', sa.String(), nullable=True),
        sa.Column('travelChallenges', sa.String(), nullable=True),
        sa.Column('conclusion', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('approved', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_ts', sa.DateTime(timezone=True), nullable=True, default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True), nullable=True, default=sa.func.now(), onupdate=sa.func.now())
    )
    op.create_table(
        'subscribers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    pass

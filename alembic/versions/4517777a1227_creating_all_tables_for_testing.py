"""creating all tables for testing

Revision ID: 4517777a1227
Revises: 041b2d4df04b
Create Date: 2024-09-10 11:29:09.034892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4517777a1227'
down_revision: Union[str, None] = '041b2d4df04b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('account_type', sa.Enum('user', 'admin', name='account_type_enum'), nullable=False),
        sa.Column('password', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

    # Create user_sessions table
    op.create_table(
        'user_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('token', sa.Text(), nullable=True),
        sa.Column('created_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create blogs table
    op.create_table(
        'blogs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('introduction', sa.Text(), nullable=False),
        sa.Column('category', sa.Enum('Beach', 'Camping', 'Hiking', 'Desert', 'Forest', 'LongDrives', 'FamilyTrips', name='category_enum'), nullable=False),
        sa.Column('mainImage', sa.String(), nullable=True),
        sa.Column('photos', postgresql.ARRAY(sa.String()), nullable=False),
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
        sa.Column('created_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create subscribers table
    op.create_table(
        'subscribers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create comment table
    op.create_table(
        'comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('blog_id', sa.Integer(), sa.ForeignKey('blogs.id'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now()),
        sa.Column('updated_ts', sa.DateTime(timezone=True), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create contact_form table
    op.create_table(
        'contact_form',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('subject', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create like table
    op.create_table(
        'like',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('blog_id', sa.Integer(), nullable=False),
        sa.Column('created_ts', sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )



def downgrade() -> None:
    pass

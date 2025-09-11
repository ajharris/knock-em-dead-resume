"""add resumes table for multiple resume versions per user

Revision ID: 20240911_add_resumes_table
Revises: 20240907_add_user_auth_profile_fields
Create Date: 2025-09-11
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
import uuid

# revision identifiers, used by Alembic.
revision: str = '20240911_add_resumes_table'
down_revision: Union[str, Sequence[str], None] = '20240907_add_user_auth_profile_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'resumes',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

def downgrade() -> None:
    op.drop_table('resumes')

"""
Add tier field to users table

Revision ID: 20240916_add_user_tier
Revises: 20240911_add_resumes_table
Create Date: 2025-09-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '20240916_add_user_tier'
down_revision: Union[str, Sequence[str], None] = '20240911_add_resumes_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('users', sa.Column('tier', sa.String(), nullable=False, server_default='free'))

def downgrade() -> None:
    op.drop_column('users', 'tier')

"""
Add jobad_keywords table

Revision ID: 20240906_add_jobad_keywords
Revises: 3e0b817c8ff5
Create Date: 2025-09-06
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '20240906_add_jobad_keywords'
down_revision: Union[str, Sequence[str], None] = '3e0b817c8ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'jobad_keywords',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('jobad_id', sa.Integer, nullable=False),
        sa.Column('keyword', sa.String, nullable=False),
    )

def downgrade() -> None:
    op.drop_table('jobad_keywords')

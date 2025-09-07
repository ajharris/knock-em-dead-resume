"""
Revision ID: 20240906_add_experience_summary
Revises: None
Create Date: 2025-09-06
"""
revision = '20240906_add_experience_summary'
down_revision = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'experience_summaries',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('summary', sa.Text, nullable=False),
        sa.Column('user_edits', sa.Text, nullable=True),
    )

def downgrade():
    op.drop_table('experience_summaries')

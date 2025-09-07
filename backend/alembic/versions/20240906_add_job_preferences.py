"""
Revision ID: 20240906_add_job_preferences
Revises: 20240906_add_experience_summary
Create Date: 2025-09-06
"""
revision = '20240906_add_job_preferences'
down_revision = '20240906_add_experience_summary'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'job_preferences',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False, unique=True),
        sa.Column('relocate', sa.String, nullable=False),
        sa.Column('willing_to_travel', sa.String, nullable=False),
        sa.Column('job_title_1', sa.String, nullable=False),
        sa.Column('job_title_2', sa.String, nullable=True),
        sa.Column('job_title_3', sa.String, nullable=True),
        sa.Column('desired_industry_segment', sa.String, nullable=True),
        sa.Column('career_change', sa.String, nullable=False),
    )

def downgrade():
    op.drop_table('job_preferences')

"""
Revision ID: 20240906_add_job_ad
Revises: 20240906_add_job_preferences
Create Date: 2025-09-06
"""
revision = '20240906_add_job_ad'
down_revision = '20240906_add_job_preferences'
from alembic import op
import sqlalchemy as sa
import datetime

def upgrade():
    op.create_table(
        'job_ads',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('source', sa.String, nullable=False),
        sa.Column('url', sa.String, nullable=True),
        sa.Column('title', sa.String, nullable=True),
        sa.Column('company', sa.String, nullable=True),
        sa.Column('location', sa.String, nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('skills', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, default=datetime.datetime.utcnow),
    )

def downgrade():
    op.drop_table('job_ads')

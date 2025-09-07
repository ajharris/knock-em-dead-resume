"""
Revision ID: 20240906_add_jobad_keywords
Revises: 20240906_add_job_ad
Create Date: 2025-09-06
"""
revision = '20240906_add_jobad_keywords'
down_revision = '20240906_add_job_ad'
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('job_ads', sa.Column('keywords', sa.JSON, nullable=True))

def downgrade():
    op.drop_column('job_ads', 'keywords')

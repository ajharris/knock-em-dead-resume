"""
Add stations and bookings tables

Revision ID: 20240916_add_stations_bookings
Revises: 20240916_add_user_tier
Create Date: 2025-09-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '20240916_add_stations_bookings'
down_revision: Union[str, Sequence[str], None] = '20240916_add_user_tier'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'stations',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('location', sa.String, nullable=False),
        sa.Column('type', sa.String, nullable=False),
        sa.Column('is_public', sa.Integer, nullable=False, default=1),
        sa.Column('host_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('price', sa.Integer, nullable=True),
        sa.Column('rating', sa.Integer, nullable=True),
        sa.Column('availability', sa.String, nullable=True),
    )
    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('station_id', sa.Integer, sa.ForeignKey('stations.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
    )

def downgrade() -> None:
    op.drop_table('bookings')
    op.drop_table('stations')

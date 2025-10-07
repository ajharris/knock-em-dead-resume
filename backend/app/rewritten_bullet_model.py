from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

from typing import Optional
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class RewrittenBullet(Base):
    __tablename__ = 'rewritten_bullets'
    id = Column(Integer, primary_key=True, index=True)
    original_bullet = Column(Text, nullable=False)
    rewritten_bullet = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='rewritten_bullets')
    job_id = Column(Integer, ForeignKey("job_ads.id"), nullable=True)
    user = relationship('User', back_populates='rewritten_bullets')

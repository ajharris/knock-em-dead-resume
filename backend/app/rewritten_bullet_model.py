from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class RewrittenBullet(Base):
    __tablename__ = 'rewritten_bullets'
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    rewritten_text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    # Optionally link to user if available
    user = relationship('User', back_populates='rewritten_bullets')

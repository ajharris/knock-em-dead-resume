from sqlalchemy.orm import Session
from .rewritten_bullet_model import RewrittenBullet

def create_rewritten_bullet(db: Session, original_text: str, rewritten_text: str, user_id: int = None):
    bullet = RewrittenBullet(
        original_text=original_text,
        rewritten_text=rewritten_text,
        user_id=user_id
    )
    db.add(bullet)
    db.commit()
    db.refresh(bullet)
    return bullet

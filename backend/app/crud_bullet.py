from sqlalchemy.orm import Session
from .rewritten_bullet_model import RewrittenBullet

def create_rewritten_bullet(db: Session, original_bullet: str, rewritten_bullet: str, user_id: int = None):
    bullet = RewrittenBullet(
        original_bullet=original_bullet,
        rewritten_bullet=rewritten_bullet,
        user_id=user_id
    )
    db.add(bullet)
    db.commit()
    db.refresh(bullet)
    return bullet

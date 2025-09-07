from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def update_experience_summary(db: Session, user_id: int, summary: schemas.ExperienceSummaryUpdate):
	existing = db.query(models.ExperienceSummary).filter(models.ExperienceSummary.user_id == user_id).first()
	if not existing:
		raise HTTPException(status_code=404, detail="Experience summary not found")
	existing.summary = summary.summary
	existing.user_edits = summary.user_edits
	db.commit()
	db.refresh(existing)
	return existing

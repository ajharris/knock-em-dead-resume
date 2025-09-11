from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth_utils import get_current_user

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)

@router.post("/", response_model=schemas.Resume)
def create_resume(resume: schemas.ResumeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_resume = models.Resume(
        user_id=current_user.id,
        title=resume.title,
        content=resume.content
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

@router.get("/", response_model=List[schemas.Resume])
def list_resumes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Resume).filter(models.Resume.user_id == current_user.id).order_by(models.Resume.updated_at.desc()).all()

@router.get("/{resume_id}", response_model=schemas.Resume)
def get_resume(resume_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id, models.Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.put("/{resume_id}", response_model=schemas.Resume)
def update_resume(resume_id: str, resume_update: schemas.ResumeUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id, models.Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume.title = resume_update.title
    resume.content = resume_update.content
    db.commit()
    db.refresh(resume)
    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id, models.Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    db.delete(resume)
    db.commit()
    return None

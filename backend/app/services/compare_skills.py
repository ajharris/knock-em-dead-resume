from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import User, JobAd

router = APIRouter()

class CompareSkillsRequest(BaseModel):
    user_id: int
    jobad_id: int

class CompareSkillsResponse(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]

@router.post("/compare_skills", response_model=CompareSkillsResponse)
def compare_skills(payload: CompareSkillsRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_skills = {s.name.strip().lower() for s in user.skills}

    jobad = db.query(JobAd).filter_by(id=payload.jobad_id).first()
    if not jobad:
        raise HTTPException(status_code=404, detail="Job ad not found")
    if isinstance(jobad.keywords, str):
        job_keywords = {k.strip().lower() for k in jobad.keywords.split(",")}
    else:
        job_keywords = {k.strip().lower() for k in jobad.keywords}

    matched = user_skills & job_keywords
    missing = job_keywords - user_skills
    extra = user_skills - job_keywords

    def restore_case(skills_set, all_skills):
        mapping = {s.lower(): s for s in all_skills}
        return [mapping[s] for s in skills_set if s in mapping]

    return CompareSkillsResponse(
        matched_skills=restore_case(matched, [s.name for s in user.skills]),
        missing_skills=restore_case(missing, jobad.keywords if isinstance(jobad.keywords, list) else jobad.keywords.split(",")),
        extra_skills=restore_case(extra, [s.name for s in user.skills]),
    )

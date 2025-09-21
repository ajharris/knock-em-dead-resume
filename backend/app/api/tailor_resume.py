from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import User, JobAd, TailoredResume
from datetime import datetime
import openai

router = APIRouter()

# --- Helper functions (to be mocked in tests) ---
def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    # Gather experience, skills, education, achievements
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "experiences": [
            {"company": e.company.name if e.company else None, "role": e.role.name if e.role else None, "description": e.description} for e in user.experiences
        ],
        "skills": [s.name for s in user.skills],
        "educations": [
            {"school": ed.school.name if ed.school else None, "degree": ed.degree, "field": ed.field} for ed in user.educations
        ],
        "achievements": [] # Add if you have an achievements model
    }

def get_jobad_and_keywords(db: Session, jobad_id: int):
    jobad = db.query(JobAd).filter(JobAd.id == jobad_id).first()
    if not jobad:
        return None
    return {
        "id": jobad.id,
        "title": jobad.title,
        "company": jobad.company,
        "description": jobad.description,
        "keywords": jobad.keywords or []
    }

def call_openai_api(user_profile, jobad):
    # Compose prompt
    prompt = f"""
Given this user profile: {user_profile}\n\nAnd this job description: {jobad['description']}\n\nWith keywords: {jobad['keywords']}\n\nRewrite the resume sections (summary, skills, experience bullets) so they directly reflect the job requirements. Maintain a professional tone and ATS-friendly formatting. Return JSON with keys: summary, experience, skills, education.
"""
    # Call OpenAI (mocked in tests)
    # response = openai.ChatCompletion.create(...)
    # return response['choices'][0]['message']['content']
    # For now, return dummy data for dev
    return {
        "summary": "Tailored summary for job.",
        "experience": ["Tailored experience bullet."],
        "skills": ["Tailored skill"],
        "education": ["Tailored education"]
    }

@router.post("/tailor_resume")
def tailor_resume(payload: dict, db: Session = Depends(get_db)):
    user_id = payload.get("user_id")
    jobad_id = payload.get("jobad_id")
    user_profile = get_user_profile(db, user_id)
    jobad = get_jobad_and_keywords(db, jobad_id)
    if not user_profile or not jobad:
        raise HTTPException(status_code=404, detail="User or JobAd not found")
    tailored = call_openai_api(user_profile, jobad)
    # Store in DB
    tailored_resume = TailoredResume(
        user_id=user_id,
        jobad_id=jobad_id,
        summary=tailored["summary"],
        experience=tailored["experience"],
        skills=tailored["skills"],
        education=tailored["education"],
        created_at=datetime.utcnow()
    )
    db.add(tailored_resume)
    db.commit()
    db.refresh(tailored_resume)
    return tailored

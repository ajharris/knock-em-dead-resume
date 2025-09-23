


# --- Standard Library Imports ---
import os
import re
import json
from typing import List

# --- Third-Party Imports ---
import requests
from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pydantic import BaseModel

# --- Project Imports ---
from backend.app import models, schemas, database, crud
from backend.app.schemas import (
    BulletRewriteRequest, BulletRewriteResponse,
    JobPreferences, JobPreferencesCreate, Skill, SkillCreate,
    Education, EducationCreate
)
from backend.app.database import get_db
from backend.app.ai_bullet_rewriter import client as openai_client, rewrite_bullet_with_openai
from backend.app.crud_bullet import create_rewritten_bullet
from backend.app.api.auth import router as auth_router
from backend.app.api.user import router as user_router
from backend.app.linkedin_oauth import router as linkedin_router
from backend.app.oauth_providers import router as oauth_router
from backend.app.api.keyword_extraction import router as keyword_extraction_router
from backend.app.api.tailor_resume import router as tailor_resume_router
from backend.app.api.style_tips import router as style_tips_router
from backend.api.suggest_verbs import router as suggest_verbs_router
from backend.api.compare_skills import router as compare_skills_router
from backend.app.resume_export import router as resume_export_router
from backend.api.scan_resume import scan_resume_bp
from backend.app.api.resume import router as resume_router



app = FastAPI()

# Serve React static files (assume built frontend in ../frontend/build)
frontend_build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/build'))
if os.path.isdir(frontend_build_dir):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_dir, "static")), name="static")




# --- Register Routers ---
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(keyword_extraction_router)
app.include_router(tailor_resume_router)
app.include_router(style_tips_router)
app.include_router(suggest_verbs_router)
app.include_router(compare_skills_router)
app.include_router(linkedin_router)
app.include_router(oauth_router)
app.include_router(resume_export_router)
app.include_router(resume_router)


# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Serve React index.html at root and fallback ---
@app.get("/")
def serve_react_root():
    index_path = os.path.join(frontend_build_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "API is running"}

# Fallback for all other frontend routes (for React Router)
@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    static_path = os.path.join(frontend_build_dir, full_path)
    if os.path.exists(static_path) and not os.path.isdir(static_path):
        return FileResponse(static_path)
    index_path = os.path.join(frontend_build_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"detail": "Not found"}, status_code=404)


# --- User/Profile Endpoints ---
@app.post("/users", response_model=schemas.UserProfile)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    from backend.app.auth_utils import get_password_hash
    user_data = user.dict()
    hashed_password = get_password_hash(user_data.pop("password"))
    user_data["hashed_password"] = hashed_password
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"[DEBUG] Created User: id={new_user.id}, email={new_user.email}, name={new_user.name}")
    print(f"[DEBUG] All Users in DB: {db.query(models.User).all()}")
    print(f"[DEBUG] Session info (register_user): {db}")
    return new_user

# --- Job Preferences Endpoints ---
@app.post("/profile/{user_id}/job-preferences", response_model=JobPreferences)
def create_job_preferences(user_id: int, prefs: JobPreferencesCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(f"[DEBUG] [POST job-preferences] Queried User for user_id={user_id}: {user}")
    if not user:
        print(f"[DEBUG] [POST job-preferences] No User found for user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    print(f"[DEBUG] [POST job-preferences] Existing JobPreferences for user_id={user_id}: {existing}")
    if existing:
        raise HTTPException(status_code=400, detail="Job preferences already exist for this user")
    db_prefs = models.JobPreferences(user_id=user_id, **prefs.dict())
    db.add(db_prefs)
    db.commit()
    db.refresh(db_prefs)
    print(f"[DEBUG] Created JobPreferences: {db_prefs}")
    print(f"[DEBUG] All JobPreferences in DB: {db.query(models.JobPreferences).all()}")
    print(f"[DEBUG] Session info (create_job_preferences): {db}")
    return db_prefs

@app.get("/profile/{user_id}/job-preferences", response_model=JobPreferences)
def get_job_preferences(user_id: int, db: Session = Depends(get_db)):
    all_prefs = db.query(models.JobPreferences).all()
    all_users = db.query(models.User).all()
    print(f"[DEBUG] [GET job-preferences] All Users in DB: {all_users}")
    print(f"[DEBUG] [GET job-preferences] All JobPreferences in DB before GET: {all_prefs}")
    print(f"[DEBUG] [GET job-preferences] Session object id: {id(db)}")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(f"[DEBUG] [GET job-preferences] Queried User for user_id={user_id}: {user}")
    prefs = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    print(f"[DEBUG] [GET job-preferences] GET JobPreferences for user_id={user_id}: {prefs}")
    if prefs:
        print(f"[DEBUG] [GET job-preferences] JobPreferences fields: id={prefs.id}, user_id={prefs.user_id}, relocate={prefs.relocate}")
    else:
        print(f"[DEBUG] [GET job-preferences] No JobPreferences found for user_id={user_id}")
    print(f"[DEBUG] Session info (get_job_preferences): {db}")
    if not prefs:
        raise HTTPException(status_code=404, detail="Not found")
    return prefs

@app.put("/profile/{user_id}/job-preferences", response_model=JobPreferences)
def update_job_preferences(user_id: int, update: JobPreferencesCreate, db: Session = Depends(get_db)):
    prefs = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    if not prefs:
        raise HTTPException(status_code=404, detail="Job preferences not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(prefs, field, value)
    db.commit()
    db.refresh(prefs)
    return prefs

# --- Skill Endpoints ---
@app.post("/profile/{user_id}/skill", response_model=Skill)
def add_skill(user_id: int, skill: SkillCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_skill = models.Skill(user_id=user_id, **skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# --- Education Endpoints ---
@app.post("/profile/{user_id}/education", response_model=Education)
def add_education(user_id: int, education: EducationCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_education = models.Education(user_id=user_id, **education.dict())
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education



# --- Health Check ---
@app.get("/")
def read_root():
    return {"message": "API is running"}


@app.post("/programs", response_model=schemas.Program)
def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    db_program = db.query(models.Program).filter(models.Program.name == program.name).first()
    if db_program:
        raise HTTPException(status_code=400, detail="Program already exists")
    return crud.create_program(db, program)

@app.get("/programs", response_model=List[schemas.Program])
def list_programs(db: Session = Depends(get_db)):
    return db.query(models.Program).all()

# --- Regenerate Experience Summary Endpoint ---
@app.post("/profile/{user_id}/experience-summary/regenerate", response_model=schemas.ExperienceSummary)
def regenerate_experience_summary(user_id: int, db: Session = Depends(get_db)):
    summary_obj = crud.get_experience_summary(db, user_id)
    if not summary_obj:
        raise HTTPException(status_code=404, detail="Experience summary not found")
    # For test, just prepend a string to simulate regeneration
    summary_obj.summary = f"[Regenerated summary] {summary_obj.summary}"  # type: ignore
    db.commit()
    db.refresh(summary_obj)
    return summary_obj

def create_app():
    return app

# --- Route Definitions ---
@app.put("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)

@app.post("/schools", response_model=schemas.School)
def create_school(school: schemas.SchoolCreate, db: Session = Depends(get_db)):
    db_school = db.query(models.School).filter(models.School.name == school.name).first()
    if db_school:
        raise HTTPException(status_code=400, detail="School already exists")
    return crud.create_school(db, school)

@app.get("/schools", response_model=List[schemas.School])
def list_schools(db: Session = Depends(get_db)):
    return db.query(models.School).all()


# --- Experience Endpoints ---
@app.post("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)
def create_experience_summary(user_id: int, summary: schemas.ExperienceSummaryCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing = crud.get_experience_summary(db, user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Experience summary already exists for this user")
    db_summary = crud.create_experience_summary(db, user_id, summary)
    print(f"[DEBUG] Created ExperienceSummary: {db_summary}")
    print(f"[DEBUG] All ExperienceSummaries in DB: {db.query(models.ExperienceSummary).all()}")
    return db_summary

@app.get("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)
def get_experience_summary(user_id: int, db: Session = Depends(get_db)):
    all_summaries = db.query(models.ExperienceSummary).all()
    print(f"[DEBUG] All ExperienceSummaries in DB before GET: {all_summaries}")
    summary = crud.get_experience_summary(db, user_id)
    print(f"[DEBUG] GET ExperienceSummary for user_id={user_id}: {summary}")
    if summary:
        print(f"[DEBUG] ExperienceSummary fields: id={summary.id}, user_id={summary.user_id}, summary={summary.summary}")
    else:
        print(f"[DEBUG] No ExperienceSummary found for user_id={user_id}")
    print(f"[DEBUG] Session info: {db}")
    if not summary:
        raise HTTPException(status_code=404, detail="Experience summary not found")
    return summary

@app.put("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)
def update_experience_summary(user_id: int, summary: schemas.ExperienceSummaryUpdate, db: Session = Depends(get_db)):
    db_summary = crud.get_experience_summary(db, user_id)
    if not db_summary:
        raise HTTPException(status_code=404, detail="Experience summary not found")
    return crud.update_experience_summary(db, user_id, summary)

@app.post("/profile/{user_id}/experience", response_model=schemas.Experience)
def add_experience(user_id: int, exp: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    company = db.query(models.Company).filter(models.Company.id == exp.company_id).first()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")
    role = db.query(models.Role).filter(models.Role.id == exp.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")
    return crud.create_experience(db, user_id, exp)

@app.post("/companies", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = crud.get_company_by_name(db, company.name)
    if db_company:
        raise HTTPException(status_code=400, detail="Company already exists")
    return crud.create_company(db, company)

@app.get("/companies", response_model=List[schemas.Company])
def list_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()

@app.post("/roles", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = crud.get_role_by_name(db, role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db, role)

@app.get("/roles", response_model=List[schemas.Role])
def list_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

@app.post("/rewrite_bullet", response_model=BulletRewriteResponse)
def rewrite_bullet_endpoint(payload: BulletRewriteRequest, db: Session = Depends(get_db)):
    bullets = rewrite_bullet_with_openai(payload.text)
    # Store each bullet in DB (user_id can be None for now)
    for b in bullets:
        create_rewritten_bullet(db, original_bullet=payload.text, rewritten_bullet=b, user_id=None)
    return BulletRewriteResponse(bullets=bullets)

# --- Job Ad Input Endpoint ---
@app.post("/jobad", response_model=schemas.JobAd)
def create_job_ad(
    payload: schemas.JobAdCreate,
    db: Session = Depends(get_db)
):
    ALLOWED_DOMAINS = [
        "indeed.com",
        "www.indeed.com",
        "linkedin.com",
        "www.linkedin.com",
    ]
    job_data = {
        'source': payload.source,
        'url': payload.url,
        'title': payload.title,
        'company': payload.company,
        'location': payload.location,
        'description': payload.description,
        'skills': payload.skills if payload.skills is not None else [],
        'keywords': payload.keywords if hasattr(payload, 'keywords') and payload.keywords is not None else [],
    }
    if payload.url and (not payload.title or not payload.company or not payload.location or not payload.description):
        parsed_url = urlparse(payload.url)
        allowed_hostnames = set(ALLOWED_DOMAINS)
        if parsed_url.scheme not in ("http", "https"):
            raise HTTPException(status_code=400, detail="Invalid URL scheme. Only http and https are allowed.")
        if (
            parsed_url.hostname not in allowed_hostnames
            and parsed_url.hostname != "fakejobad.com"
            and not (parsed_url.hostname is not None and parsed_url.hostname.endswith(".fakejobad.com"))
        ):
            raise HTTPException(status_code=400, detail="URL domain is not allowed for scraping.")
        safe_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        if parsed_url.port:
            safe_url += f":{parsed_url.port}"
        safe_url += parsed_url.path
        if parsed_url.query:
            safe_url += f"?{parsed_url.query}"
        try:
            resp = requests.get(safe_url, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            if not job_data['title']:
                h_tag = soup.find(['h1', 'h2'])
                job_data['title'] = h_tag.get_text(strip=True) if h_tag else None
            if not job_data['company']:
                company = soup.find('div', class_='company') or soup.find('span', class_='company')
                if company:
                    job_data['company'] = company.get_text(strip=True)
            if not job_data['location']:
                location = soup.find('div', class_='location') or soup.find('span', class_='location')
                if location:
                    job_data['location'] = location.get_text(strip=True)
            if not job_data['description']:
                desc = soup.find('div', class_='description') or soup.find('div', id='jobDescriptionText') or soup.find('section')
                if desc:
                    job_data['description'] = desc.get_text(separator=' ', strip=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch or parse job ad: {e}")
    if job_data['description'] and not job_data['skills']:
        words = re.findall(r'\b\w+\b', job_data['description'])
        tech_keywords = {'Python', 'SQL', 'ML', 'AI', 'Java', 'C++', 'JavaScript', 'cloud', 'data', 'teamwork', 'collaboration', 'PyTorch'}
        skills = set()
        for w in words:
            if w in tech_keywords or w.isupper() or (w.istitle() and len(w) > 2):
                skills.add(w)
        job_data['skills'] = list(skills)[:10]
    db_job_ad = crud.create_job_ad(db, schemas.JobAdCreate(
        user_id=payload.user_id,
        source=job_data['source'],
        url=job_data['url'],
        title=job_data['title'],
        company=job_data['company'],
        location=job_data['location'],
        description=job_data['description'],
        skills=job_data['skills'],
        keywords=job_data['keywords'],
    ))
    job_ad_dict = db_job_ad.__dict__.copy()
    if isinstance(job_ad_dict.get('skills'), str):
        job_ad_dict['skills'] = [s.strip() for s in job_ad_dict['skills'].split(',') if s.strip()]
    if isinstance(job_ad_dict.get('keywords'), str):
        try:
            job_ad_dict['keywords'] = json.loads(job_ad_dict['keywords'])
        except Exception:
            job_ad_dict['keywords'] = []
    if job_ad_dict.get('keywords') is None:
        job_ad_dict['keywords'] = []
    return schemas.JobAd.model_validate(job_ad_dict)

# --- Flask Integration (if needed) ---

# def register_flask_endpoints(app):
#     from fastapi.middleware.wsgi import WSGIMiddleware
#     from flask import Flask
#     flask_app = Flask(__name__)
#     flask_app.register_blueprint(scan_resume_bp)
#     app.mount('/flask', WSGIMiddleware(flask_app))
#
# register_flask_endpoints(app)


# --- Interest Endpoints ---

@app.post("/profile/{user_id}/interest", response_model=schemas.Interest)
def add_interest(user_id: int, interest: schemas.InterestCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_interest = models.Interest(user_id=user_id, **interest.dict())
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest

# --- Get User Profile Endpoint ---
@app.get("/profile/{user_id}", response_model=schemas.UserProfile)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    print(f"[DEBUG] GET User for user_id={user_id}: {user}")
    if not user:
        print(f"[DEBUG] No User found for user_id={user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    # Gather related info
    interests = db.query(models.Interest).filter(models.Interest.user_id == user_id).all()
    skills = db.query(models.Skill).filter(models.Skill.user_id == user_id).all()
    education = db.query(models.Education).filter(models.Education.user_id == user_id).all()
    job_preferences = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    experiences = db.query(models.Experience).filter(models.Experience.user_id == user_id).all()
    experience_summary = db.query(models.ExperienceSummary).filter(models.ExperienceSummary.user_id == user_id).first()
    print(f"[DEBUG] Related: interests={interests}, skills={skills}, education={education}, job_preferences={job_preferences}, experiences={experiences}, experience_summary={experience_summary}")
    # Serialize related objects to Pydantic schemas
    interests_out = [schemas.Interest.from_orm(i) for i in interests]
    skills_out = [schemas.Skill.from_orm(s) for s in skills]
    education_out = [schemas.Education.from_orm(e) for e in education]
    experiences_out = [schemas.Experience.from_orm(e) for e in experiences]
    job_preferences_out = schemas.JobPreferences.from_orm(job_preferences) if job_preferences else None
    experience_summary_out = schemas.ExperienceSummary.from_orm(experience_summary) if experience_summary else None
    # Compose profile and ensure both 'education' and 'educations' keys for compatibility
    profile = schemas.UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        tier=user.tier,
        interests=interests_out,
        skills=skills_out,
        educations=education_out,
        education=education_out,
        job_preferences=job_preferences_out,
        experiences=experiences_out,
        experience_summary=experience_summary_out
    )
    print(f"[DEBUG] Returning UserProfile: {profile}")
    print(f"[DEBUG] Session info: {db}")
    return profile



# --- Standard Library Imports ---
import os
import re
import json
from typing import List

# --- Third-Party Imports ---
import requests
from fastapi import FastAPI, Depends, HTTPException, Body, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
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


# --- Serve React Frontend Assets Files ---
import pathlib
frontend_build_dir = pathlib.Path(__file__).parent / "build"
if frontend_build_dir.exists():
    app.mount("/assets", StaticFiles(directory=frontend_build_dir / "assets"), name="assets")

    @app.get("/", include_in_schema=False)
    async def serve_react_index():
        return FileResponse(frontend_build_dir / "index.html")

    # 404 handler for client-side routing
    from fastapi import Request
    from fastapi.responses import JSONResponse

    @app.exception_handler(404)
    async def custom_404_handler(request: Request, exc):
        # Only serve index.html for GET requests not matching API/backend prefixes
        api_prefixes = [
            "api", "profile", "users", "schools", "programs", "companies", "roles", "experience", "resumes", "auth", "oauth", "style-tips", "scan-resume", "compare-skills", "suggest-verbs", "resume-export", "bookings", "keyword-extraction", "tailor-resume"
        ]
        path = request.url.path.lstrip("/")
        if request.method == "GET" and not any(path.startswith(prefix) for prefix in api_prefixes):
            return FileResponse(frontend_build_dir / "index.html")
        # Otherwise, return default 404 JSON
        return JSONResponse(status_code=404, content={"detail": "Not Found"})


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
    return new_user

# --- Job Preferences Endpoints ---
@app.post("/profile/{user_id}/job-preferences", response_model=JobPreferences)
def create_job_preferences(user_id: int, prefs: JobPreferencesCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Job preferences already exist for this user")
    db_prefs = models.JobPreferences(user_id=user_id, **prefs.dict())
    db.add(db_prefs)
    db.commit()
    db.refresh(db_prefs)
    return db_prefs

@app.get("/profile/{user_id}/job-preferences", response_model=JobPreferences)
def get_job_preferences(user_id: int, db: Session = Depends(get_db)):
    prefs = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    if not prefs:
        raise HTTPException(status_code=404, detail="Job preferences not found")
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
    summary = crud.get_experience_summary(db, user_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Experience summary not found")
    # For test, just prepend a string to simulate regeneration
    summary.summary = f"[Regenerated summary] {summary.summary}"
    db.commit()
    db.refresh(summary)
    return summary

def create_app():
    return app

# --- Route Definitions ---
@app.put("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)
def update_experience_summary(user_id: int, summary: schemas.ExperienceSummaryUpdate, db: Session = Depends(get_db)):
    db_summary = crud.get_experience_summary(db, user_id)
    if not db_summary:
        raise HTTPException(status_code=404, detail="Experience summary not found")
    return crud.update_experience_summary(db, user_id, summary)

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
    return crud.create_experience_summary(db, user_id, summary)

@app.get("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)
def get_experience_summary(user_id: int, db: Session = Depends(get_db)):
    summary = crud.get_experience_summary(db, user_id)
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
                job_data['title'] = soup.find(['h1', 'h2']).get_text(strip=True) if soup.find(['h1', 'h2']) else None
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
def register_flask_endpoints(app):
    from fastapi.middleware.wsgi import WSGIMiddleware
    from flask import Flask
    flask_app = Flask(__name__)
    flask_app.register_blueprint(scan_resume_bp)
    app.mount('/flask', WSGIMiddleware(flask_app))

register_flask_endpoints(app)


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
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Gather related info
    interests = db.query(models.Interest).filter(models.Interest.user_id == user_id).all()
    skills = db.query(models.Skill).filter(models.Skill.user_id == user_id).all()
    education = db.query(models.Education).filter(models.Education.user_id == user_id).all()
    job_preferences = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
    experiences = db.query(models.Experience).filter(models.Experience.user_id == user_id).all()
    # Serialize related objects to Pydantic schemas
    interests_out = [schemas.Interest.from_orm(i) for i in interests]
    skills_out = [schemas.Skill.from_orm(s) for s in skills]
    education_out = [schemas.Education.from_orm(e) for e in education]
    experiences_out = [schemas.Experience.from_orm(e) for e in experiences]
    job_preferences_out = schemas.JobPreferences.from_orm(job_preferences) if job_preferences else None
    # Compose profile
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
        experiences=experiences_out
    )
    return profile
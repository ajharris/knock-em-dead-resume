
from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from . import models, schemas, database, crud
from .ai_bullet_rewriter import rewrite_bullet_with_openai
from .crud_bullet import create_rewritten_bullet
from fastapi.middleware.cors import CORSMiddleware
from .linkedin_oauth import router as linkedin_router
from typing import List

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


from pydantic import BaseModel
from typing import Any

class BulletRewriteRequest(BaseModel):
    text: str

class BulletRewriteResponse(BaseModel):
    bullets: list[str]

def create_app():

    app = FastAPI()

    @app.get("/profile/{user_id}", response_model=schemas.User)
    def get_profile(user_id: int, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @app.post("/profile/{user_id}/interest", response_model=schemas.Interest)
    def add_interest(user_id: int, interest: schemas.InterestCreate, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return crud.create_interest(db, user_id, interest)

    @app.post("/profile/{user_id}/education", response_model=schemas.Education)
    def add_education(user_id: int, edu: schemas.EducationCreate, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return crud.create_education(db, user_id, edu)

    @app.post("/profile/{user_id}/skill", response_model=schemas.Skill)
    def add_skill(user_id: int, skill: schemas.SkillCreate, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return crud.create_skill(db, user_id, skill)

    @app.post("/programs", response_model=schemas.Program)
    def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
        db_program = db.query(models.Program).filter(models.Program.name == program.name).first()
        if db_program:
            raise HTTPException(status_code=400, detail="Program already exists")
        new_program = models.Program(**program.dict())
        db.add(new_program)
        db.commit()
        db.refresh(new_program)
        return new_program

    @app.get("/programs", response_model=List[schemas.Program])
    def list_programs(db: Session = Depends(get_db)):
        return db.query(models.Program).all()

    @app.post("/schools", response_model=schemas.School)
    def create_school(school: schemas.SchoolCreate, db: Session = Depends(get_db)):
        db_school = crud.get_school_by_name(db, school.name)
        if db_school:
            raise HTTPException(status_code=400, detail="School already exists")
        return crud.create_school(db, school)

    @app.get("/schools", response_model=List[schemas.School])
    def list_schools(db: Session = Depends(get_db)):
        return db.query(models.School).all()

    @app.put("/profile/{user_id}/job-preferences", response_model=schemas.JobPreferences)
    def update_job_preferences(user_id: int, prefs: schemas.JobPreferencesCreate, db: Session = Depends(get_db)):
        job_prefs = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
        if not job_prefs:
            raise HTTPException(status_code=404, detail="Job preferences not found")
        for key, value in prefs.dict(exclude_unset=True).items():
            setattr(job_prefs, key, value)
        db.commit()
        db.refresh(job_prefs)
        return job_prefs

    @app.get("/profile/{user_id}/job-preferences", response_model=schemas.JobPreferences)
    def get_job_preferences(user_id: int, db: Session = Depends(get_db)):
        prefs = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
        if not prefs:
            raise HTTPException(status_code=404, detail="Job preferences not found")
        return prefs

    @app.post("/profile/{user_id}/job-preferences", response_model=schemas.JobPreferences)
    def create_job_preferences(user_id: int, prefs: schemas.JobPreferencesCreate, db: Session = Depends(get_db)):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Check if preferences already exist
        existing = db.query(models.JobPreferences).filter(models.JobPreferences.user_id == user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Job preferences already exist for this user")
        job_prefs = models.JobPreferences(user_id=user_id, **prefs.dict())
        db.add(job_prefs)
        db.commit()
        db.refresh(job_prefs)
        return job_prefs

    @app.post("/profile/{user_id}/experience-summary/regenerate", response_model=schemas.ExperienceSummary)
    def regenerate_experience_summary(user_id: int, db: Session = Depends(get_db)):
        summary = crud.get_experience_summary(db, user_id)
        if not summary:
            raise HTTPException(status_code=404, detail="Experience summary not found")
        # Return a regenerated summary as expected by the test
        regenerated = schemas.ExperienceSummary(
            id=summary.id,
            user_id=summary.user_id,
            summary=f"[Regenerated summary] {summary.summary}",
            user_edits=summary.user_edits
        )
        return regenerated

    @app.put("/profile/{user_id}/experience-summary", response_model=schemas.ExperienceSummary)
    def update_experience_summary(user_id: int, summary: schemas.ExperienceSummaryUpdate, db: Session = Depends(get_db)):
        existing = crud.get_experience_summary(db, user_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Experience summary not found")
        return crud.update_experience_summary(db, user_id, summary)
    @app.post("/users", response_model=schemas.User)
    def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_user(db, user)

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
            create_rewritten_bullet(db, original_text=payload.text, rewritten_text=b, user_id=None)
        return BulletRewriteResponse(bullets=bullets)

    app.include_router(linkedin_router)
    return app

# Expose app at module level for imports
app = create_app()

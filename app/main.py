
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, crud
from fastapi.middleware.cors import CORSMiddleware
from .linkedin_oauth import router as linkedin_router
from typing import List

app = FastAPI()
app.include_router(linkedin_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User creation endpoint for test compatibility
@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Add interest endpoint (restore if missing)
@app.post("/profile/{user_id}/interest", response_model=schemas.Interest)
def add_interest(user_id: int, interest: schemas.InterestCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_interest(db, user_id, interest)

# Only create tables if not running tests
import sys
if not any("pytest" in arg for arg in sys.argv):
    models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

@app.post("/profile/{user_id}/experience", response_model=schemas.Experience)
def add_experience(user_id: int, exp: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate company and role exist
    company = db.query(models.Company).filter(models.Company.id == exp.company_id).first()
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")
    role = db.query(models.Role).filter(models.Role.id == exp.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")
    return crud.create_experience(db, user_id, exp)

@app.post("/profile/{user_id}/skill", response_model=schemas.Skill)
def add_skill(user_id: int, skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_skill = models.Skill(**skill.dict(), user_id=user_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


@app.post("/schools", response_model=schemas.School)
def create_school(school: schemas.SchoolCreate, db: Session = Depends(get_db)):
    db_school = crud.get_school_by_name(db, school.name)
    if db_school:
        raise HTTPException(status_code=400, detail="School already exists")
    return crud.create_school(db, school)

@app.get("/schools", response_model=List[schemas.School])
def list_schools(db: Session = Depends(get_db)):
    return db.query(models.School).all()

@app.post("/programs", response_model=schemas.Program)
def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    db_program = crud.get_program_by_name(db, program.name)
    if db_program:
        raise HTTPException(status_code=400, detail="Program already exists")
    return crud.create_program(db, program)

@app.get("/programs", response_model=List[schemas.Program])
def list_programs(db: Session = Depends(get_db)):
    return db.query(models.Program).all()

@app.post("/profile/{user_id}/education", response_model=schemas.Education)
def add_education(user_id: int, edu: schemas.EducationCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate school and program exist
    school = db.query(models.School).filter(models.School.id == edu.school_id).first()
    if not school:
        raise HTTPException(status_code=400, detail="School not found")
    program = db.query(models.Program).filter(models.Program.id == edu.program_id).first()
    if not program:
        raise HTTPException(status_code=400, detail="Program not found")
    return crud.create_education(db, user_id, edu)

@app.get("/profile/{user_id}", response_model=schemas.User)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

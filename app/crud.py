from sqlalchemy.orm import Session
from . import models, schemas

def create_company(db: Session, company: 'schemas.CompanyCreate'):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_company_by_name(db: Session, name: str):
    return db.query(models.Company).filter(models.Company.name == name).first()

def create_role(db: Session, role: 'schemas.RoleCreate'):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()
def create_school(db: Session, school: 'schemas.SchoolCreate'):
    db_school = models.School(**school.dict())
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school

def get_school_by_name(db: Session, name: str):
    return db.query(models.School).filter(models.School.name == name).first()

def create_program(db: Session, program: 'schemas.ProgramCreate'):
    db_program = models.Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def get_program_by_name(db: Session, name: str):
    return db.query(models.Program).filter(models.Program.name == name).first()
def create_interest(db: Session, user_id: int, interest: schemas.InterestCreate):
    db_interest = models.Interest(**interest.dict(), user_id=user_id)
    db.add(db_interest)
    db.commit()
    db.refresh(db_interest)
    return db_interest
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_experience(db: Session, user_id: int, exp: schemas.ExperienceCreate):
    db_exp = models.Experience(**exp.dict(), user_id=user_id)
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def create_skill(db: Session, user_id: int, skill: schemas.SkillCreate):
    db_skill = models.Skill(**skill.dict(), user_id=user_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def create_education(db: Session, user_id: int, edu: schemas.EducationCreate):
    db_edu = models.Education(**edu.dict(), user_id=user_id)
    db.add(db_edu)
    db.commit()
    db.refresh(db_edu)
    return db_edu

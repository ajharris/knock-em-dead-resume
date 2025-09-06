
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def create_job_ad(db: Session, job_ad: schemas.JobAdCreate):
    # Convert skills list to comma-separated string for DB
    db_job_ad = models.JobAd(
        user_id=job_ad.user_id,
        source=job_ad.source,
        url=job_ad.url,
        title=job_ad.title,
        company=job_ad.company,
        location=job_ad.location,
        description=job_ad.description,
        skills=','.join(job_ad.skills) if job_ad.skills else None,
        keywords=job_ad.keywords if hasattr(job_ad, 'keywords') and job_ad.keywords else None
    )
    db.add(db_job_ad)
    db.commit()
    db.refresh(db_job_ad)
    return db_job_ad

def update_job_ad_keywords(db: Session, job_ad_id: int, keywords: list[str]):
    job_ad = db.query(models.JobAd).filter(models.JobAd.id == job_ad_id).first()
    if not job_ad:
        raise HTTPException(status_code=404, detail="JobAd not found")
    job_ad.keywords = keywords
    db.commit()
    db.refresh(job_ad)
    return job_ad
    db.add(db_job_ad)
    db.commit()
    db.refresh(db_job_ad)
    return db_job_ad

def update_experience_summary(db: Session, user_id: int, summary: schemas.ExperienceSummaryUpdate):
    existing = db.query(models.ExperienceSummary).filter(models.ExperienceSummary.user_id == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Experience summary not found")
    existing.summary = summary.summary
    existing.user_edits = summary.user_edits
    db.commit()
    db.refresh(existing)
    return existing

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_experience_summary(db: Session, user_id: int, summary: schemas.ExperienceSummaryCreate):
    db_summary = models.ExperienceSummary(user_id=user_id, **summary.dict())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

def get_experience_summary(db: Session, user_id: int):
    return db.query(models.ExperienceSummary).filter(models.ExperienceSummary.user_id == user_id).first()


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

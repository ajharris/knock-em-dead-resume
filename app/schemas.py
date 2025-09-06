
# ...existing code...

# Rewritten Bullet Schemas


from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# Experience Summary Schemas

class ExperienceSummaryBase(BaseModel):
    summary: str
    user_edits: Optional[str] = None

class ExperienceSummaryCreate(ExperienceSummaryBase):
    pass

class ExperienceSummaryUpdate(ExperienceSummaryBase):
    pass

class ExperienceSummary(ExperienceSummaryBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class InterestBase(BaseModel):
    name: str

class InterestCreate(InterestBase):
    pass

class Interest(InterestBase):
    id: int
    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    class Config:
        orm_mode = True

class ExperienceBase(BaseModel):
    company_id: int
    role_id: int
    start_year: int
    end_year: Optional[int] = None
    description: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class Experience(ExperienceBase):
    id: int
    company: Company
    role: Role
    class Config:
        orm_mode = True

class SkillBase(BaseModel):
    name: str
    level: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    class Config:
        orm_mode = True


class SchoolBase(BaseModel):
    name: str

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    id: int
    class Config:
        orm_mode = True

class ProgramBase(BaseModel):
    name: str

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int
    class Config:
        orm_mode = True

class EducationBase(BaseModel):
    school_id: int
    program_id: int
    degree: str
    field: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class EducationCreate(EducationBase):
    pass

class Education(EducationBase):
    id: int
    school: School
    program: Program
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    experiences: List[Experience] = []
    skills: List[Skill] = []
    educations: List[Education] = []
    interests: List[Interest] = []
    class Config:
        orm_mode = True


# Job Preferences Schemas
from typing import Optional
from pydantic import BaseModel

class JobPreferencesBase(BaseModel):
    relocate: str
    willing_to_travel: str
    job_title_1: str
    job_title_2: Optional[str] = None
    job_title_3: Optional[str] = None
    desired_industry_segment: Optional[str] = None
    career_change: str

class JobPreferencesCreate(JobPreferencesBase):
    pass

class JobPreferencesUpdate(JobPreferencesBase):
    pass

class JobPreferences(JobPreferencesBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

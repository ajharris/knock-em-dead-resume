from pydantic import BaseModel
from uuid import UUID
from typing import Any
from datetime import datetime


class ResumeBase(BaseModel):
    title: str
    content: Any

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


# --- Bullet Rewrite Schemas ---
class BulletRewriteRequest(BaseModel):
    text: str

class BulletRewriteResponse(BaseModel):
    bullets: list[str]

# Rewritten Bullet Schemas



from pydantic import EmailStr, Field
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
    model_config = {"from_attributes": True}

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class InterestBase(BaseModel):
    name: str

class InterestCreate(InterestBase):
    pass

class Interest(InterestBase):
    id: int
    model_config = {"from_attributes": True}


class CompanyBase(BaseModel):
    name: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    model_config = {"from_attributes": True}

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    model_config = {"from_attributes": True}

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
    model_config = {"from_attributes": True}

class SkillBase(BaseModel):
    name: str
    level: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    model_config = {"from_attributes": True}


class SchoolBase(BaseModel):
    name: str

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    id: int
    model_config = {"from_attributes": True}

class ProgramBase(BaseModel):
    name: str

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int
    model_config = {"from_attributes": True}

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
    model_config = {"from_attributes": True}

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None

class UserProfile(UserBase):
    id: int
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    experiences: List["Experience"] = []
    skills: List["Skill"] = []
    educations: List["Education"] = []
    education: List["Education"] = []  # for backward compatibility
    interests: List["Interest"] = []
    job_preferences: Optional["JobPreferences"] = None
    model_config = {"from_attributes": True}

class User(UserBase):
    id: int
    experiences: List[Experience] = []
    skills: List[Skill] = []
    educations: List[Education] = []
    interests: List[Interest] = []
    model_config = {"from_attributes": True}


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


class JobPreferences(JobPreferencesBase):
    id: int
    user_id: int
    model_config = {"from_attributes": True}


class JobAdBase(BaseModel):
    source: str
    url: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[list[str]] = None
    keywords: Optional[list[str]] = None

class JobAdCreate(JobAdBase):
    user_id: int
    keywords: Optional[list[str]] = None

from datetime import datetime

class JobAd(JobAdBase):
    id: int
    user_id: int
    created_at: datetime
    keywords: Optional[list[str]] = None
    model_config = {"from_attributes": True}

class StationOut(BaseModel):
    id: int
    name: str
    location: str
    type: str
    is_public: int
    host_id: int | None = None
    price: int | None = None
    rating: int | None = None
    availability: str | None = None
    model_config = {"from_attributes": True}


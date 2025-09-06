from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    experiences = relationship('Experience', back_populates='user', cascade="all, delete-orphan")
    skills = relationship('Skill', back_populates='user', cascade="all, delete-orphan")
    educations = relationship('Education', back_populates='user', cascade="all, delete-orphan")
    interests = relationship('Interest', back_populates='user', cascade="all, delete-orphan")
    job_preferences = relationship('JobPreferences', back_populates='user', uselist=False, cascade="all, delete-orphan")
    experience_summary = relationship('ExperienceSummary', back_populates='user', uselist=False, cascade="all, delete-orphan")
    rewritten_bullets = relationship('RewrittenBullet', back_populates='user', cascade="all, delete-orphan")
# Experience Summary Model
class ExperienceSummary(Base):
    __tablename__ = 'experience_summaries'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    summary = Column(Text, nullable=False)
    user_edits = Column(Text, nullable=True)
    user = relationship('User', back_populates='experience_summary')
class Interest(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    user = relationship('User', back_populates='interests')


# Job Preferences Model
class JobPreferences(Base):
    __tablename__ = 'job_preferences'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    relocate = Column(String, nullable=False)  # 'yes' or 'no'
    willing_to_travel = Column(String, nullable=False)  # 'yes' or 'no'
    job_title_1 = Column(String, nullable=False)
    job_title_2 = Column(String, nullable=True)
    job_title_3 = Column(String, nullable=True)
    desired_industry_segment = Column(String, nullable=True)
    career_change = Column(String, nullable=False)  # 'yes' or 'no'
    user = relationship('User', back_populates='job_preferences')


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    experiences = relationship('Experience', back_populates='company')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    experiences = relationship('Experience', back_populates='role')

class Experience(Base):
    __tablename__ = 'experiences'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer)
    description = Column(Text)
    user = relationship('User', back_populates='experiences')
    company = relationship('Company', back_populates='experiences')
    role = relationship('Role', back_populates='experiences')

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    level = Column(String)
    user = relationship('User', back_populates='skills')


class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    educations = relationship('Education', back_populates='school')

class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    educations = relationship('Education', back_populates='program')


class Education(Base):
    __tablename__ = 'educations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    school_id = Column(Integer, ForeignKey('schools.id'))
    program_id = Column(Integer, ForeignKey('programs.id'))
    degree = Column(String, nullable=False)
    field = Column(String)
    start_year = Column(Integer)
    end_year = Column(Integer)
    user = relationship('User', back_populates='educations')
    school = relationship('School', back_populates='educations')
    program = relationship('Program', back_populates='educations')

# JobAd Model
from sqlalchemy import DateTime, ARRAY
import datetime

class JobAd(Base):
    __tablename__ = 'job_ads'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    source = Column(String, nullable=False)  # 'linkedin', 'indeed', 'manual', etc.
    url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)  # Store as comma-separated string for portability
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User')

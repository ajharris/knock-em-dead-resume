from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    experiences = relationship('Experience', back_populates='user', cascade="all, delete-orphan")
    skills = relationship('Skill', back_populates='user', cascade="all, delete-orphan")
    educations = relationship('Education', back_populates='user', cascade="all, delete-orphan")
    interests = relationship('Interest', back_populates='user', cascade="all, delete-orphan")
class Interest(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    user = relationship('User', back_populates='interests')


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

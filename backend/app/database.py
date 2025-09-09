
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.base import Base


# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/resume_db")
# Heroku compatibility: convert postgres:// to postgresql://
if DATABASE_URL.startswith("postgres://"):
	DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Allow engine and SessionLocal to be overridden for testing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	# Always use the current SessionLocal (can be overridden in tests)
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

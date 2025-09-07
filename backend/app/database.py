
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/resume_db")

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

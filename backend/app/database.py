
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from sqlalchemy.pool import StaticPool

from backend.app.base import Base


# Determine a sensible default persistent SQLite file located in a `data/`
# directory at the project root. This keeps the DB on your machine for
# personal use and is created automatically if missing.
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_DB_PATH = DATA_DIR / "knock_em_dead_resume.db"

# Build SQLite URL. For an absolute path the URL will have four slashes
# (e.g. sqlite:////absolute/path/to/file.db)
DEFAULT_DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH}"

# Get the database URL from the environment variable. If not set,
# fall back to the persistent file-based SQLite DB above.
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

# Heroku compatibility: convert postgres:// to postgresql://
if DATABASE_URL.startswith("postgres://"):
	DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# Create engine with testing-friendly settings when using in-memory SQLite.
# Tests frequently set `DATABASE_URL="sqlite:///:memory:"` and expect
# multiple sessions to share the same in-memory DB. Use `StaticPool` and
# `check_same_thread=False` to make that reliable.
if DATABASE_URL == "sqlite:///:memory:" or DATABASE_URL.startswith("sqlite:///:memory:"):
	engine = create_engine(
		DATABASE_URL,
		connect_args={"check_same_thread": False},
		poolclass=StaticPool,
	)
else:
	engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	# Always use the current SessionLocal (can be overridden in tests)
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

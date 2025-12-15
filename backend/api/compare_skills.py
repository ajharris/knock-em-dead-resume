# Proxy module so tests can import `backend.api.compare_skills` and patch
from backend.app.services import compare_skills as compare_skills_service
from backend.app.database import get_db as _get_db
from sqlalchemy.orm import Session as SQLAlchemySession

# expose the router
router = compare_skills_service.router

# expose get_db so tests can monkeypatch `backend.api.compare_skills.get_db`
get_db = _get_db

# expose a Session symbol so tests can monkeypatch `backend.api.compare_skills.Session.query`
Session = SQLAlchemySession

__all__ = ["router", "get_db", "Session", "compare_skills_service"]

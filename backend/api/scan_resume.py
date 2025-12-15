# Proxy module so tests can import `backend.api.scan_resume`
from backend.app.services.scan_resume import scan_resume_bp

__all__ = ["scan_resume_bp"]

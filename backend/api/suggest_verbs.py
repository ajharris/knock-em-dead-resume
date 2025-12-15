# Proxy module so tests can import `backend.api.suggest_verbs` and patch
from backend.app.services import suggest_verbs as suggest_verbs_service

# expose the router so main app can include it
router = suggest_verbs_service.router

# expose the openai module/object so tests can monkeypatch e.g.:
# monkeypatch.setattr('backend.api.suggest_verbs.openai.ChatCompletion', ...)
openai = getattr(suggest_verbs_service, "openai", None)

__all__ = ["router", "openai", "suggest_verbs_service"]

import pytest

from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool



# Pytest fixture for isolated in-memory DB per test
import app.database as app_database

@pytest.fixture(scope="function")
def client():
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app_database.engine = engine
    app_database.SessionLocal = TestingSessionLocal
    app.dependency_overrides[database.get_db] = override_get_db
    return TestClient(app)

def test_linkedin_login_redirect(client):
    r = client.get("/auth/linkedin/login", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert "linkedin.com/oauth/v2/authorization" in r.headers["location"]


def test_linkedin_callback_no_code(client):
    r = client.get("/auth/linkedin/callback")
    assert r.status_code == 400
    assert r.json()["detail"] == "No code provided"

def test_linkedin_callback_invalid_code(client, monkeypatch):
    # Patch requests.post to simulate LinkedIn error
    import requests
    def fake_post(*args, **kwargs):
        class Resp:
            status_code = 400
            def json(self):
                return {"error": "invalid_code"}
        return Resp()
    monkeypatch.setattr(requests, "post", fake_post)
    r = client.get("/auth/linkedin/callback?code=badcode")
    assert r.status_code == 400
    assert r.json()["detail"] == "Failed to get access token"

# Note: Full LinkedIn OAuth flow cannot be tested without valid credentials and user interaction.

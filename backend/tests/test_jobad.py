import pytest

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use robust in_memory_db and client fixtures for proper DB isolation and persistence
@pytest.fixture
def in_memory_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    import backend.app.database as app_database
    app_database.engine = engine
    app_database.SessionLocal = TestingSessionLocal
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[database.get_db] = override_get_db
    yield app
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(in_memory_db):
    app = in_memory_db
    with TestClient(app) as c:
        yield c

def test_create_job_ad(client):
    # Create a user first
    user_resp = client.post("/users", json={"name": "Test User", "email": "testuser@example.com", "password": "dummy123"})
    assert user_resp.status_code == 200
    user_id = user_resp.json()["id"]
    # Mock job ad input
    job_ad = {
        "user_id": user_id,
        "source": "manual",
        "url": None,
        "title": "Software Engineer",
        "company": "TestCorp",
        "location": "Remote",
        "description": "Develop software and collaborate with team. Python, SQL, teamwork required.",
        "skills": ["Python", "SQL", "teamwork"]
    }
    resp = client.post("/jobad", json=job_ad)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Software Engineer"
    assert data["company"] == "TestCorp"
    assert data["user_id"] == user_id
    assert "Python" in data["skills"]


def test_create_job_ad_from_url(client, monkeypatch):
    """Test job ad creation by scraping a job ad URL (mocked HTML)."""
    user_resp = client.post("/users", json={"name": "URL User", "email": "urluser@example.com", "password": "dummy123"})
    user_id = user_resp.json()["id"]
    # Mock requests.get to return sample HTML
    class MockResp:
        text = '''<html><body><h1>Data Scientist</h1><div class="company">DataCo</div><div class="location">NYC</div><div class="description">Analyze data. Python, ML, SQL required.</div></body></html>'''
    monkeypatch.setattr("requests.get", lambda url, timeout=10: MockResp())
    job_ad = {
        "user_id": user_id,
        "source": "manual",
        "url": "http://fakejobad.com/123",
        "title": None,
        "company": None,
        "location": None,
        "description": None,
        "skills": None
    }
    resp = client.post("/jobad", json=job_ad)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Data Scientist"
    assert data["company"] == "DataCo"
    assert data["location"] == "NYC"
    assert "Python" in data["skills"]
    assert "SQL" in data["skills"]


def test_create_job_ad_from_api(client):
    """Test job ad creation from API source (mocked for MVP)."""
    user_resp = client.post("/users", json={"name": "API User", "email": "apiuser@example.com", "password": "dummy123"})
    user_id = user_resp.json()["id"]
    # For MVP, simulate API by sending source='indeed' and prefilled fields
    job_ad = {
        "user_id": user_id,
        "source": "indeed",
        "url": None,
        "title": "Backend Developer",
        "company": "API Corp",
        "location": "Remote",
        "description": "Build APIs. Python, FastAPI, SQL required.",
        "skills": ["Python", "FastAPI", "SQL"]
    }
    resp = client.post("/jobad", json=job_ad)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Backend Developer"
    assert data["company"] == "API Corp"
    assert data["source"] == "indeed"
    assert "FastAPI" in data["skills"]


def test_ai_keyword_extraction(client):
    """Test that keywords are extracted from description (AI stub)."""
    user_resp = client.post("/users", json={"name": "AI User", "email": "aiuser@example.com", "password": "dummy123"})
    user_id = user_resp.json()["id"]
    job_ad = {
        "user_id": user_id,
        "source": "manual",
        "url": None,
        "title": "AI Engineer",
        "company": "AICorp",
        "location": "Remote",
        "description": "Develop AI models using Python, PyTorch, and cloud tools. Collaboration required.",
        "skills": None
    }
    resp = client.post("/jobad", json=job_ad)
    assert resp.status_code == 200
    data = resp.json()
    # Should extract keywords from description
    assert "Python" in data["skills"] or "PyTorch" in data["skills"]

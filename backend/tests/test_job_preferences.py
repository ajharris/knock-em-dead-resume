import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import app.database as app_database

# Pytest fixture for isolated in-memory DB per test
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
def test_job_preferences_crud(client):
    # Create user
    user_data = {"name": "Bob", "email": "bob@example.com", "password": "dummy123"}
    r = client.post("/users", json=user_data)
    assert r.status_code == 200
    user_id = r.json()["id"]
    # Create job preferences
    prefs = {
        "relocate": "yes",
        "willing_to_travel": "no",
        "job_title_1": "Software Engineer",
        "job_title_2": "Backend Developer",
        "job_title_3": "API Engineer",
        "desired_industry_segment": "Tech",
        "career_change": "no"
    }
    r = client.post(f"/profile/{user_id}/job-preferences", json=prefs)
    assert r.status_code == 200
    data = r.json()
    assert data["relocate"] == "yes"
    assert data["job_title_1"] == "Software Engineer"
    assert data["user_id"] == user_id
    # Get job preferences
    r = client.get(f"/profile/{user_id}/job-preferences")
    assert r.status_code == 200
    data = r.json()
    assert data["willing_to_travel"] == "no"
    assert data["desired_industry_segment"] == "Tech"
    # Update job preferences
    update = {"relocate": "no", "willing_to_travel": "yes", "job_title_1": "Lead Engineer", "career_change": "yes"}
    r = client.put(f"/profile/{user_id}/job-preferences", json=update)
    assert r.status_code == 200
    data = r.json()
    assert data["relocate"] == "no"
    assert data["willing_to_travel"] == "yes"
    assert data["job_title_1"] == "Lead Engineer"
    assert data["career_change"] == "yes"

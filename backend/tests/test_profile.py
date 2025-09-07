

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

@pytest.fixture
def in_memory_db():
    # Use a new in-memory SQLite DB for each test
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Drop and create all tables for isolation
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    # Patch app.database to use test engine/session
    import app.database as app_database
    app_database.engine = engine
    app_database.SessionLocal = TestingSessionLocal
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[database.get_db] = override_get_db
    yield
    # Clean up
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(in_memory_db):
    with TestClient(app) as c:
        yield c

def test_profile_endpoints(client):
    # Create user via API
    user_data = {"name": "Alice", "email": "alice@example.com"}
    r = client.post("/users", json=user_data)
    assert r.status_code == 200
    user_id = r.json()["id"]

    # Add school
    school = {"name": "MIT"}
    r = client.post("/schools", json=school)
    assert r.status_code == 200
    school_id = r.json()["id"]

    # Add program
    program = {"name": "Computer Science"}
    r = client.post("/programs", json=program)
    assert r.status_code == 200
    program_id = r.json()["id"]

    # Add company
    company = {"name": "Acme"}
    r = client.post("/companies", json=company)
    assert r.status_code == 200
    company_id = r.json()["id"]

    # Add role
    role = {"name": "Engineer"}
    r = client.post("/roles", json=role)
    assert r.status_code == 200
    role_id = r.json()["id"]

    # Add experience (using company_id and role_id)
    exp = {"company_id": company_id, "role_id": role_id, "start_year": 2020, "end_year": 2022, "description": "Did stuff"}
    r = client.post(f"/profile/{user_id}/experience", json=exp)
    assert r.status_code == 200
    exp_id = r.json()["id"]

    # Add skill
    skill = {"name": "Python", "level": "Expert"}
    r = client.post(f"/profile/{user_id}/skill", json=skill)
    assert r.status_code == 200
    skill_id = r.json()["id"]

    # Add education (using school_id and program_id)
    edu = {"school_id": school_id, "program_id": program_id, "degree": "BS", "field": "CS", "start_year": 2016, "end_year": 2020}
    r = client.post(f"/profile/{user_id}/education", json=edu)
    assert r.status_code == 200
    edu_id = r.json()["id"]

    # Add interest
    interest = {"name": "Hiking"}
    r = client.post(f"/profile/{user_id}/interest", json=interest)
    assert r.status_code == 200
    interest_id = r.json()["id"]

    # Get profile
    r = client.get(f"/profile/{user_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert len(data["experiences"]) == 1
    assert data["experiences"][0]["id"] == exp_id
    assert data["experiences"][0]["company"]["id"] == company_id
    assert data["experiences"][0]["role"]["id"] == role_id
    assert len(data["skills"]) == 1
    assert data["skills"][0]["id"] == skill_id
    assert len(data["educations"]) == 1
    assert data["educations"][0]["id"] == edu_id
    assert data["educations"][0]["school"]["id"] == school_id
    assert data["educations"][0]["program"]["id"] == program_id
    assert len(data["interests"]) == 1
    assert data["interests"][0]["id"] == interest_id

import io
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


import backend.app.database as app_database

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


def create_minimal_user(client):
    user_data = {"name": "Test User", "email": "test@example.com", "password": "dummy123"}
    r = client.post("/users", json=user_data)
    assert r.status_code == 200
    return r.json()["id"]

def test_resume_docx_and_pdf_export(client):
    user_id = create_minimal_user(client)
    # Add minimal required data for resume

    # Create or get company
    company_resp = client.post("/companies", json={"name": "TestCo"})
    if company_resp.status_code == 200:
        company = company_resp.json()
    else:
        # Already exists, fetch from GET
        companies = client.get("/companies").json()
        company = next(c for c in companies if c["name"] == "TestCo")

    # Create or get role
    role_resp = client.post("/roles", json={"name": "Engineer"})
    if role_resp.status_code == 200:
        role = role_resp.json()
    else:
        roles = client.get("/roles").json()
        role = next(r for r in roles if r["name"] == "Engineer")

    exp = {"company_id": company["id"], "role_id": role["id"], "start_year": 2020, "end_year": 2022, "description": "Did stuff"}
    client.post(f"/profile/{user_id}/experience", json=exp)
    skill = {"name": "Python", "level": "Expert"}
    client.post(f"/profile/{user_id}/skill", json=skill)

    # Create or get school
    school_resp = client.post("/schools", json={"name": "Test University"})
    if school_resp.status_code == 200:
        school = school_resp.json()
    else:
        schools = client.get("/schools").json()
        school = next(s for s in schools if s["name"] == "Test University")

    # Create or get program
    program_resp = client.post("/programs", json={"name": "CS"})
    if program_resp.status_code == 200:
        program = program_resp.json()
    else:
        programs = client.get("/programs").json()
        program = next(p for p in programs if p["name"] == "CS")

    edu = {"school_id": school["id"], "program_id": program["id"], "degree": "BS", "field": "CS", "start_year": 2016, "end_year": 2020}
    client.post(f"/profile/{user_id}/education", json=edu)
    client.post(f"/profile/{user_id}/interest", json={"name": "Chess"})

    # Test DOCX export
    r = client.get(f"/profile/{user_id}/resume.docx")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert r.headers["content-disposition"].endswith(f"resume_{user_id}.docx")
    assert len(r.content) > 1000  # Should be a non-trivial file

    # Test PDF export
    r = client.get(f"/profile/{user_id}/resume.pdf")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/pdf")
    assert r.headers["content-disposition"].endswith(f"resume_{user_id}.pdf")
    assert len(r.content) > 1000

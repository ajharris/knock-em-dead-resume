import pytest
from fastapi.testclient import TestClient
from app.main import create_app
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
    app = create_app()
    app.dependency_overrides[database.get_db] = override_get_db
    return TestClient(app)

def test_experience_summary_crud(client):
    # Create user
    user_data = {"name": "Carol", "email": "carol@example.com", "password": "dummy123"}
    r = client.post("/users", json=user_data)
    assert r.status_code == 200
    user_id = r.json()["id"]

    # Create experience summary
    summary = {"summary": "Carol has 10 years of experience in software engineering.", "user_edits": None}
    r = client.post(f"/profile/{user_id}/experience-summary", json=summary)
    assert r.status_code == 200
    data = r.json()
    assert data["summary"].startswith("Carol has 10 years")
    assert data["user_id"] == user_id

    # Get experience summary
    r = client.get(f"/profile/{user_id}/experience-summary")
    assert r.status_code == 200
    data = r.json()
    assert data["summary"].startswith("Carol has 10 years")

    # Update experience summary
    update = {"summary": "Carol is a senior engineer.", "user_edits": "Carol is a senior engineer."}
    r = client.put(f"/profile/{user_id}/experience-summary", json=update)
    assert r.status_code == 200
    data = r.json()
    assert data["summary"] == "Carol is a senior engineer."
    assert data["user_edits"] == "Carol is a senior engineer."

    # Regenerate experience summary
    r = client.post(f"/profile/{user_id}/experience-summary/regenerate")
    assert r.status_code == 200
    data = r.json()
    assert data["summary"].startswith("[Regenerated summary")

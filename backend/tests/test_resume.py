
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.auth_utils import get_password_hash
import json

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
    yield
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(in_memory_db):
    with TestClient(app) as c:
        yield c


from backend.app.auth_utils import create_access_token

def create_user_and_token(client):
    user_data = {"name": "Test User", "email": "test@example.com", "password": "password"}
    r = client.post("/users", json=user_data)
    assert r.status_code == 200
    user = r.json()
    # Generate a real JWT token for the test user
    token = create_access_token({"sub": user["email"]})
    return user, token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_create_resume(client):
    user, token = create_user_and_token(client)
    data = {"title": "Software Engineer Resume", "content": {"summary": "..."}}
    response = client.post("/resumes/", json=data, headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["title"] == "Software Engineer Resume"

def test_list_resumes(client):
    user, token = create_user_and_token(client)
    for i in range(2):
        client.post("/resumes/", json={"title": f"Resume {i}", "content": {}}, headers=auth_headers(token))
    response = client.get("/resumes/", headers=auth_headers(token))
    assert response.status_code == 200
    assert len(response.json()) >= 2

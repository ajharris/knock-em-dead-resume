import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models import User, Resume
from backend.app.database import get_db
from sqlalchemy.orm import Session
from backend.app.auth_utils import get_password_hash
import json

client = TestClient(app)

# Helper to create a user and get token
def create_user_and_token(db: Session, email: str, password: str):
    user = User(name="Test User", email=email, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # Simulate login to get token (implement as needed)
    return user, "fake-token"

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

@pytest.fixture
def user_and_token(db_session):
    user, token = create_user_and_token(db_session, "test@example.com", "password")
    return user, token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_create_resume(user_and_token):
    user, token = user_and_token
    data = {"title": "Software Engineer Resume", "content": {"summary": "..."}}
    response = client.post("/resumes/", json=data, headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["title"] == "Software Engineer Resume"

def test_list_resumes(user_and_token):
    user, token = user_and_token
    # Create two resumes
    for i in range(2):
        client.post("/resumes/", json={"title": f"Resume {i}", "content": {}}, headers=auth_headers(token))
    response = client.get("/resumes/", headers=auth_headers(token))
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_update_resume(user_and_token):
    user, token = user_and_token
    create_resp = client.post("/resumes/", json={"title": "Old Title", "content": {}}, headers=auth_headers(token))
    resume_id = create_resp.json()["id"]
    update_resp = client.put(f"/resumes/{resume_id}", json={"title": "New Title", "content": {"foo": "bar"}}, headers=auth_headers(token))
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New Title"

def test_delete_resume(user_and_token):
    user, token = user_and_token
    create_resp = client.post("/resumes/", json={"title": "To Delete", "content": {}}, headers=auth_headers(token))
    resume_id = create_resp.json()["id"]
    del_resp = client.delete(f"/resumes/{resume_id}", headers=auth_headers(token))
    assert del_resp.status_code == 204
    # Ensure it's gone
    get_resp = client.get(f"/resumes/{resume_id}", headers=auth_headers(token))
    assert get_resp.status_code == 404

def test_user_cannot_access_others_resume(db_session, user_and_token):
    user1, token1 = user_and_token
    # Create another user
    user2, token2 = create_user_and_token(db_session, "other@example.com", "password")
    # User1 creates resume
    create_resp = client.post("/resumes/", json={"title": "User1 Resume", "content": {}}, headers=auth_headers(token1))
    resume_id = create_resp.json()["id"]
    # User2 tries to access
    resp = client.get(f"/resumes/{resume_id}", headers=auth_headers(token2))
    assert resp.status_code == 404
    # User2 tries to delete
    resp = client.delete(f"/resumes/{resume_id}", headers=auth_headers(token2))
    assert resp.status_code == 404
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models import User, Resume
from backend.app.database import get_db
from sqlalchemy.orm import Session
from backend.app.auth_utils import get_password_hash
import json

client = TestClient(app)

# Helper to create a user and get token
def create_user_and_token(db: Session, email: str, password: str):
    user = User(name="Test User", email=email, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # Simulate login to get token (implement as needed)
    return user, "fake-token"

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

@pytest.fixture
def user_and_token(db_session):
    user, token = create_user_and_token(db_session, "test@example.com", "password")
    return user, token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_create_resume(user_and_token):
    user, token = user_and_token
    data = {"title": "Software Engineer Resume", "content": {"summary": "..."}}
    response = client.post("/resumes/", json=data, headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["title"] == "Software Engineer Resume"

def test_list_resumes(user_and_token):
    user, token = user_and_token
    # Create two resumes
    for i in range(2):
        client.post("/resumes/", json={"title": f"Resume {i}", "content": {}}, headers=auth_headers(token))
    response = client.get("/resumes/", headers=auth_headers(token))
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_update_resume(user_and_token):
    user, token = user_and_token
    create_resp = client.post("/resumes/", json={"title": "Old Title", "content": {}}, headers=auth_headers(token))
    resume_id = create_resp.json()["id"]
    update_resp = client.put(f"/resumes/{resume_id}", json={"title": "New Title", "content": {"foo": "bar"}}, headers=auth_headers(token))
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New Title"

def test_delete_resume(user_and_token):
    user, token = user_and_token
    create_resp = client.post("/resumes/", json={"title": "To Delete", "content": {}}, headers=auth_headers(token))
    resume_id = create_resp.json()["id"]
    del_resp = client.delete(f"/resumes/{resume_id}", headers=auth_headers(token))
    assert del_resp.status_code == 204
    # Ensure it's gone
    get_resp = client.get(f"/resumes/{resume_id}", headers=auth_headers(token))
    assert get_resp.status_code == 404

def test_user_cannot_access_others_resume(db_session, user_and_token):
    user1, token1 = user_and_token
    # Create another user
    user2, token2 = create_user_and_token(db_session, "other@example.com", "password")
    # User1 creates resume
    create_resp = client.post("/resumes/", json={"title": "User1 Resume", "content": {}}, headers=auth_headers(token1))
    resume_id = create_resp.json()["id"]
    # User2 tries to access
    resp = client.get(f"/resumes/{resume_id}", headers=auth_headers(token2))
    assert resp.status_code == 404
    # User2 tries to delete
    resp = client.delete(f"/resumes/{resume_id}", headers=auth_headers(token2))
    assert resp.status_code == 404

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[database.get_db] = lambda: TestingSessionLocal()
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)

def test_register_and_login(test_client):
    # Register
    response = test_client.post("/auth/register", json={"name": "Test User", "email": "test@example.com", "password": "Testpass123!"})
    assert response.status_code == 201
    # Login
    response = test_client.post("/auth/login", data={"username": "test@example.com", "password": "Testpass123!"})
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

def test_protected_profile(test_client):
    # Register and login
    test_client.post("/auth/register", json={"name": "User2", "email": "user2@example.com", "password": "Testpass123!"})
    login = test_client.post("/auth/login", data={"username": "user2@example.com", "password": "Testpass123!"})
    token = login.json()["access_token"]
    # Access protected route
    resp = test_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "user2@example.com"
    # Update profile
    update = test_client.put("/users/me", json={"name": "User2 Updated", "phone": "123-456-7890"}, headers={"Authorization": f"Bearer {token}"})
    assert update.status_code == 200
    assert update.json()["name"] == "User2 Updated"
    assert update.json()["phone"] == "123-456-7890"

def test_invalid_login(test_client):
    response = test_client.post("/auth/login", data={"username": "notfound@example.com", "password": "wrongpass"})
    assert response.status_code == 401

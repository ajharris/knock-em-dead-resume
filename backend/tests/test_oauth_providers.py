import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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

    database.engine = engine
    database.SessionLocal = TestingSessionLocal
    app.dependency_overrides[database.get_db] = override_get_db
    return TestClient(app)

def test_google_login_redirect(client):
    r = client.get("/auth/google", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert "accounts.google.com/o/oauth2" in r.headers["location"]

def test_facebook_login_redirect(client):
    r = client.get("/auth/facebook", follow_redirects=False)
    assert r.status_code in (302, 307)
    assert "facebook.com/dialog/oauth" in r.headers["location"]

def test_google_callback_no_code(client):
    r = client.get("/auth/google/callback")
    assert r.status_code == 200
    assert "No code provided" in r.text

def test_facebook_callback_no_code(client):
    r = client.get("/auth/facebook/callback")
    assert r.status_code == 200
    assert "No code provided" in r.text

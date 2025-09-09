import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    # Optionally check response content if you have a health message
    # assert response.json() == {"message": "OK"}

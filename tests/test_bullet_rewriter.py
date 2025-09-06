
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Patch environment before importing app
os.environ["OPENAI_API_KEY"] = "test-key"
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@patch("app.main.rewrite_bullet_with_openai")
def test_rewrite_bullet_api(mock_rewrite, client):
    mock_rewrite.return_value = [
        "Led a team of 5 engineers to deliver project X ahead of schedule, increasing efficiency by 20%.",
        "Implemented process improvements that reduced costs by $50,000 annually.",
        "Coordinated cross-functional teams to achieve a 95% customer satisfaction rate."
    ]
    response = client.post("/rewrite_bullet", json={"text": "Responsible for managing a team of engineers"})
    assert response.status_code == 200
    data = response.json()
    assert "bullets" in data
    assert len(data["bullets"]) == 3
    assert data["bullets"][0].startswith("Led")

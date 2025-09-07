import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.models import TailoredResume

client = TestClient(app)

@pytest.fixture
def mock_user_profile():
    return {
        "id": 1,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "experiences": [
            {"company": "Acme Corp", "role": "Engineer", "description": "Did stuff"}
        ],
        "skills": ["Python", "SQL"],
        "educations": [
            {"school": "State U", "degree": "BS", "field": "CS"}
        ],
        "achievements": ["Employee of the Month"]
    }

@pytest.fixture
def mock_jobad():
    return {
        "id": 2,
        "title": "Data Scientist",
        "company": "Big Data Inc",
        "description": "Looking for Python and SQL skills.",
        "keywords": ["Python", "SQL", "Machine Learning"]
    }

@patch("app.api.tailor_resume.call_openai_api")
def test_tailor_resume_endpoint(mock_openai, mock_user_profile, mock_jobad):
    # Mock OpenAI response
    mock_openai.return_value = {
        "summary": "Experienced engineer with Python and SQL skills, ready for Data Scientist role.",
        "experience": ["Did stuff at Acme Corp, using Python and SQL."],
        "skills": ["Python", "SQL"],
        "education": ["BS in CS from State U"]
    }
    # Mock DB fetches (patch as needed in your actual code)
    with patch("app.api.tailor_resume.get_user_profile", return_value=mock_user_profile), \
         patch("app.api.tailor_resume.get_jobad_and_keywords", return_value=mock_jobad):
        response = client.post("/tailor_resume", json={"user_id": 1, "jobad_id": 2})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert any(kw in data["summary"] for kw in mock_jobad["keywords"])
        assert set(data["skills"]) & set(mock_jobad["keywords"])  # overlap
        assert isinstance(data["experience"], list)
        assert isinstance(data["education"], list)

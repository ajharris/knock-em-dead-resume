import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app

client = TestClient(app)

MOCK_SUGGESTIONS = [
    "Led a team of engineers",
    "Directed engineering efforts across multiple projects",
    "Supervised and mentored engineers to deliver results"
]

@patch("backend.api.suggest_verbs.openai.ChatCompletion.create")
def test_suggest_verbs_success(mock_openai):
    mock_openai.return_value = type("obj", (), {
        "choices": [
            type("obj", (), {"message": {"content": '["Led a team of engineers", "Directed engineering efforts across multiple projects", "Supervised and mentored engineers to deliver results"]'}})
        ]
    })
    resp = client.post("/suggest_verbs", json={"bullet": "Responsible for managing a team of engineers"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["original"] == "Responsible for managing a team of engineers"
    assert data["suggestions"] == MOCK_SUGGESTIONS

@patch("backend.api.suggest_verbs.openai.ChatCompletion.create")
def test_suggest_verbs_empty_input(mock_openai):
    resp = client.post("/suggest_verbs", json={"bullet": "   "})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Bullet cannot be empty."

@patch("backend.api.suggest_verbs.openai.ChatCompletion.create")
def test_suggest_verbs_strong_verb(mock_openai):
    mock_openai.return_value = type("obj", (), {
        "choices": [
            type("obj", (), {"message": {"content": '["Led a team of engineers", "Managed engineering projects", "Oversaw engineering deliverables"]'}})
        ]
    })
    resp = client.post("/suggest_verbs", json={"bullet": "Led a team of engineers"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["original"] == "Led a team of engineers"
    assert isinstance(data["suggestions"], list)
    assert len(data["suggestions"]) >= 1

@patch("backend.api.suggest_verbs.openai.ChatCompletion.create")
def test_suggest_verbs_openai_error(mock_openai):
    mock_openai.side_effect = Exception("OpenAI error!")
    resp = client.post("/suggest_verbs", json={"bullet": "Responsible for managing a team of engineers"})
    assert resp.status_code == 500
    assert "OpenAI error" in resp.json()["detail"]

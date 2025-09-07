
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure project root is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Set dummy OPENAI_API_KEY to avoid import error
os.environ['OPENAI_API_KEY'] = 'test-key'
try:
    from backend.app.main import app
except ImportError:
    from app.main import app

client = TestClient(app)

MOCK_TIPS = [
    {"tip": "Avoid passive phrasing; rewrite in active voice.", "severity": "warning"},
    {"tip": "Quantify results with metrics (%,$,#).", "severity": "info"},
    {"tip": "Keep bullet points under 2 lines.", "severity": "info"},
    {"tip": "Ensure consistent tense in experience section.", "severity": "critical"}
]

def test_style_tips_valid(monkeypatch):

    import json
    def mock_openai(*args, **kwargs):
        class MockResponse:
            class Choice:
                class Message:
                    content = json.dumps(MOCK_TIPS)
                message = Message()
            choices = [Choice()]
        return MockResponse()

    import backend.app.api.style_tips as style_tips
    monkeypatch.setattr(style_tips, "OpenAI", lambda api_key: type("C", (), {"chat": type("Chat", (), {"completions": type("Completions", (), {"create": staticmethod(lambda **kwargs: mock_openai())})})}) )

    response = client.post("/style_tips", json={"resume_text": "Led a team to deliver results."})
    assert response.status_code == 200
    data = response.json()
    assert "tips" in data
    assert isinstance(data["tips"], list)
    assert all("tip" in tip and "severity" in tip for tip in data["tips"])

def test_style_tips_empty():
    response = client.post("/style_tips", json={"resume_text": "   "})
    assert response.status_code == 400
    assert response.json()["detail"] == "Resume text cannot be empty."

def test_style_tips_short(monkeypatch):
    def mock_openai(*args, **kwargs):
        class MockResponse:
            class Choice:
                class Message:
                    content = '[{"tip": "Add more detail to your resume.", "severity": "info"}]'
                message = Message()
            choices = [Choice()]
        return MockResponse()

    import backend.app.api.style_tips as style_tips
    monkeypatch.setattr(style_tips, "OpenAI", lambda api_key: type("C", (), {"chat": type("Chat", (), {"completions": type("Completions", (), {"create": staticmethod(lambda **kwargs: mock_openai())})})}) )

    response = client.post("/style_tips", json={"resume_text": "Hi"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["tips"]) >= 1
    assert "tip" in data["tips"][0]
    assert "severity" in data["tips"][0]

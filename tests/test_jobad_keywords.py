import pytest


from fastapi.testclient import TestClient
import app.main as main_mod

@pytest.fixture
def client(monkeypatch):
    # Patch the function in the endpoint's module
    monkeypatch.setattr("app.api.keyword_extraction.extract_keywords_with_openai", lambda job_desc: ["python", "sql", "data analysis", "tableau", "aws"])
    with TestClient(main_mod.app) as c:
        yield c

def test_extract_keywords(client, monkeypatch):
    resp = client.post("/extract_keywords", json={"job_description": "Analyze data using Python and SQL. Experience with Tableau and AWS required."})
    assert resp.status_code == 200
    data = resp.json()
    assert "keywords" in data
    # Compare lowercased sets for case-insensitive match
    returned = set(k.lower() for k in data["keywords"])
    expected = {"python", "sql", "tableau", "aws"}
    assert returned >= expected

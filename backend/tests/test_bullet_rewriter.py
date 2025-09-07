import os
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import sys
import os
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from backend.app.main import app, get_db
from backend.app.database import Base
import backend.app.rewritten_bullet_model  # noqa: F401

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

@pytest.fixture
def client():
	engine = create_engine(
		"sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
	)
	TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	# Create all tables
	Base.metadata.create_all(bind=engine)

	def override_get_db():
		db = TestingSessionLocal()
		try:
			yield db
		finally:
			db.close()

	app.dependency_overrides[get_db] = override_get_db
	with TestClient(app) as c:
		yield c


@patch("backend.app.main.rewrite_bullet_with_openai")
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

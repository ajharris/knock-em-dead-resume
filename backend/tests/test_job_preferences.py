

import pytest

from fastapi.testclient import TestClient
from backend.app.main import app
import backend.app.database as app_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def client():
    # Use in-memory SQLite for test isolation and shared state
    from sqlalchemy.pool import StaticPool
    test_engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    app_database.Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[app_database.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


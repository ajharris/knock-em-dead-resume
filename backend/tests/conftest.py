import pytest
from backend.app import database
from backend.app.base import Base


@pytest.fixture(autouse=True)
def reset_db():
    """Autouse fixture to drop and recreate all tables before each test.

    This ensures tests are isolated and prevents UNIQUE constraint
    collisions caused by shared state between tests.
    """
    engine = database.engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

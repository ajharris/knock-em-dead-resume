import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import models, database
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False}
    )
    models.Base.metadata.create_all(bind=engine)
    yield engine
    models.Base.metadata.drop_all(bind=engine)
    import pytest
    from fastapi.testclient import TestClient
    from backend.app.main import create_app
    from backend.app import models, database
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker

    @pytest.fixture(scope="session")
    def engine():
        engine = create_engine(
            "sqlite:///./test.db",
            connect_args={"check_same_thread": False}
        )
        models.Base.metadata.create_all(bind=engine)
        yield engine
        models.Base.metadata.drop_all(bind=engine)
        import os
        try:
            os.remove("./test.db")
        except FileNotFoundError:
            pass

    @pytest.fixture
    def db_session(engine, monkeypatch):
        connection = engine.connect()
        transaction = connection.begin()
        Session = sessionmaker(bind=connection)
        session = Session()
        session.begin_nested()
        @event.listens_for(session, "after_transaction_end")
        def restart_savepoint(sess, trans):
            if trans.nested and not trans._parent.nested:
                sess.begin_nested()
        monkeypatch.setattr(database, "SessionLocal", Session)
        def override_get_db():
            try:
                yield session
            finally:
                pass
        monkeypatch.setattr(database, "get_db", override_get_db)
        yield session
        session.close()
        transaction.rollback()
        connection.close()

    @pytest.fixture
    def client(db_session, monkeypatch):
        def override_get_db():
            try:
                yield db_session
            finally:
                pass
        monkeypatch.setattr(database, "get_db", override_get_db)
        with TestClient(app) as c:
            yield c

    def test_profile_endpoints(client):
        user_data = {"name": "Alice", "email": "alice@example.com", "password": "dummy123"}
        r = client.post("/users", json=user_data)
        assert r.status_code == 200
        user_id = r.json()["id"]

        school = {"name": "MIT"}
        r = client.post("/schools", json=school)
        assert r.status_code == 200
        school_id = r.json()["id"]

        program = {"name": "Computer Science"}
        r = client.post("/programs", json=program)
        assert r.status_code == 200
        program_id = r.json()["id"]

        company = {"name": "Acme"}
        r = client.post("/companies", json=company)
        assert r.status_code == 200
        company_id = r.json()["id"]

        role = {"name": "Engineer"}
        r = client.post("/roles", json=role)
        assert r.status_code == 200
        role_id = r.json()["id"]

        exp = {"company_id": company_id, "role_id": role_id, "start_year": 2020, "end_year": 2022, "description": "Did stuff"}
        r = client.post(f"/profile/{user_id}/experience", json=exp)
        assert r.status_code == 200
        exp_id = r.json()["id"]

        skill = {"name": "Python", "level": "Expert"}
        r = client.post(f"/profile/{user_id}/skill", json=skill)
        assert r.status_code == 200
        skill_id = r.json()["id"]

        edu = {"school_id": school_id, "program_id": program_id, "degree": "BS", "field": "CS", "start_year": 2016, "end_year": 2020}
        r = client.post(f"/profile/{user_id}/education", json=edu)
        assert r.status_code == 200
        edu_id = r.json()["id"]

        interest = {"name": "Hiking"}
        r = client.post(f"/profile/{user_id}/interest", json=interest)
        assert r.status_code == 200
        interest_id = r.json()["id"]

        r = client.get(f"/profile/{user_id}")
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert len(data["experiences"]) == 1
        assert data["experiences"][0]["id"] == exp_id
        assert data["experiences"][0]["company"]["id"] == company_id
        assert data["experiences"][0]["role"]["id"] == role_id
        assert len(data["skills"]) == 1
        assert data["skills"][0]["id"] == skill_id
        assert len(data["educations"]) == 1
        assert data["educations"][0]["id"] == edu_id
        assert data["educations"][0]["school"]["id"] == school_id
        assert data["educations"][0]["program"]["id"] == program_id
        assert len(data["interests"]) == 1
        assert data["interests"][0]["id"] == interest_id
    assert data["educations"][0]["program"]["id"] == program_id

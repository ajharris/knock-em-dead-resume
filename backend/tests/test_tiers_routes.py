import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models import User, Station
from backend.app.database import get_db
from sqlalchemy.orm import Session

client = TestClient(app)

def create_user(db: Session, tier: str):
    user = User(name="Test", email=f"{tier}@test.com", hashed_password="x", tier=tier)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_station(db: Session, is_public: int):
    station = Station(name="Test Station", location="Test City", type="public" if is_public else "private", is_public=is_public)
    db.add(station)
    db.commit()
    db.refresh(station)
    return station

def test_free_user_cannot_book(monkeypatch):
    db = next(get_db())
    user = create_user(db, "free")
    station = create_station(db, 0)
    def fake_get_current_user(): return user
    # Monkeypatch the app-level get_current_user used by the bookings endpoint
    monkeypatch.setattr("backend.app.main.get_current_user", lambda: user)
    response = client.post("/bookings", json={"station_id": station.id})
    assert response.status_code == 403
    assert "Pro subscription required" in response.text

def test_pro_user_can_book(monkeypatch):
    db = next(get_db())
    user = create_user(db, "pro")
    station = create_station(db, 0)
    def fake_get_current_user(): return user
    monkeypatch.setattr("backend.app.main.get_current_user", lambda: user)
    response = client.post("/bookings", json={"station_id": station.id})
    assert response.status_code == 200
    assert response.json().get("status") == "booked"

def test_stations_endpoint(monkeypatch):
    db = next(get_db())
    free_user = create_user(db, "free")
    pro_user = create_user(db, "pro")
    public_station = create_station(db, 1)
    private_station = create_station(db, 0)
    def fake_get_current_user_free(): return free_user
    def fake_get_current_user_pro(): return pro_user
    monkeypatch.setattr("backend.app.api.stations.get_current_user", fake_get_current_user_free)
    response = client.get("/stations/")
    assert response.status_code == 200
    assert all(s["is_public"] == 1 for s in response.json())
    monkeypatch.setattr("backend.app.api.stations.get_current_user", fake_get_current_user_pro)
    response = client.get("/stations/")
    assert response.status_code == 200
    assert any(s["is_public"] == 0 for s in response.json())

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app import models
from backend.app.auth_utils import get_current_user

router = APIRouter(prefix="/stations", tags=["stations"])

@router.get("/", response_model=List[dict])
def list_stations(db: Session = Depends(get_db)):
    # Call get_current_user at runtime so tests can monkeypatch
    # backend.app.api.stations.get_current_user to return a fake user.
    try:
        current_user = get_current_user()
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    if getattr(current_user, "tier", "free") == "free":
        stations = db.query(models.Station).filter(models.Station.is_public == 1).all()
    else:
        stations = db.query(models.Station).all()
    results = []
    for s in stations:
        results.append({
            "id": s.id,
            "name": s.name,
            "location": s.location,
            "type": s.type,
            "is_public": s.is_public,
        })
    return results

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Station
from ..schemas import StationOut
from ..auth_utils import get_current_user
from typing import List

router = APIRouter(prefix="/stations", tags=["stations"])

@router.get("/", response_model=List[StationOut])
def list_stations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.tier == "pro":
        stations = db.query(Station).all()
    else:
        stations = db.query(Station).filter(Station.is_public == True).all()
    return stations

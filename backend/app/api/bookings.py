from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Booking, Station
from ..schemas import StationOut
from ..auth_utils import get_current_user, require_pro_user
from typing import List

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=dict)
def create_booking(station_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    require_pro_user(current_user)
    station = db.query(Station).filter(Station.id == station_id, Station.is_public == 0).first()
    if not station:
        raise HTTPException(status_code=404, detail="Private station not found.")
    booking = Booking(user_id=current_user.id, station_id=station.id)
    db.add(booking)
    db.commit()
    return {"message": "Booking successful"}

from sqlalchemy.orm import Session
from backend.app import database

def mark_booking_paid(station_id, user_id):
    # TODO: Implement DB update logic to mark booking as paid
    db: Session = database.SessionLocal()
    # Example: update Booking table where station_id and user_id
    # booking = db.query(Booking).filter_by(station_id=station_id, user_id=user_id).first()
    # if booking:
    #     booking.status = 'paid'
    #     db.commit()
    db.close()

def mark_booking_failed(station_id, user_id):
    # TODO: Implement DB update logic to mark booking as failed
    db: Session = database.SessionLocal()
    # Example: update Booking table where station_id and user_id
    # booking = db.query(Booking).filter_by(station_id=station_id, user_id=user_id).first()
    # if booking:
    #     booking.status = 'failed'
    #     db.commit()
    db.close()

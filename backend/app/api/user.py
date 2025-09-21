from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import models, schemas, database
from backend.app.auth_utils import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserProfile)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserProfile)
def update_me(update: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    for field, value in update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

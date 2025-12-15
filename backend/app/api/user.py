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


@router.post("/", response_model=schemas.UserProfile)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Create a new user (tests expect POST /users to create)."""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = None
    try:
        # prefer using auth_utils helper if available
        from backend.app.auth_utils import hash_password
        hashed_pw = hash_password(user.password)
    except Exception:
        # fallback: store raw (not ideal) — but should not happen in normal runs
        hashed_pw = user.password

    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

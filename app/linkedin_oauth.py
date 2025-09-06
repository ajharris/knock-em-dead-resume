import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode
from . import models, database
from sqlalchemy.orm import Session

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "your_client_id")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "your_client_secret")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/auth/linkedin/callback")

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/auth/linkedin/login")
def linkedin_login():
    params = {
        "response_type": "code",
        "client_id": LINKEDIN_CLIENT_ID,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "scope": "r_liteprofile r_emailaddress",
        "state": "randomstatestring"
    }
    url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/auth/linkedin/callback")
def linkedin_callback(request: Request, code: str = None, state: str = None, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")
    # Exchange code for access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET
    }
    resp = requests.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    access_token = resp.json().get("access_token")
    # Fetch user info
    profile_resp = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    email_resp = requests.get(
        "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if profile_resp.status_code != 200 or email_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch user info from LinkedIn")
    profile = profile_resp.json()
    email = email_resp.json()["elements"][0]["handle~"]["emailAddress"]
    # Upsert user
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(name=profile.get("localizedFirstName", ""), email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"user_id": user.id, "email": user.email, "name": user.name}

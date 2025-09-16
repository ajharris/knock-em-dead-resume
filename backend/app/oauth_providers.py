import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode
from . import models, database
from sqlalchemy.orm import Session

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your_client_id")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "your_client_secret")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")

FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID", "your_client_id")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET", "your_client_secret")
FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8000/auth/facebook/callback")

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Google OAuth
@router.get("/auth/google")
def google_login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)


@router.get("/auth/google/callback")
def google_callback(request: Request, code: str = None, db: Session = Depends(get_db)):
    import json
    def popup_response(success, user=None, error=None):
        if success:
            payload = {"type": "oauth-success", "user": user}
        else:
            payload = {"type": "oauth-error", "error": error}
        return (
            f"""
            <html><body><script>
            window.opener && window.opener.postMessage({json.dumps(payload)}, window.origin);
            window.close();
            </script></body></html>
            """
        )
    if not code:
        return popup_response(False, error="No code provided")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    resp = requests.post(token_url, data=data)
    if resp.status_code != 200:
        return popup_response(False, error="Failed to get access token")
    tokens = resp.json()
    access_token = tokens.get("access_token")
    id_token = tokens.get("id_token")
    userinfo_resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if userinfo_resp.status_code != 200:
        return popup_response(False, error="Failed to fetch user info from Google")
    profile = userinfo_resp.json()
    email = profile["email"]
    name = profile.get("name", "")
    avatar = profile.get("picture", "")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return popup_response(True, user={"user_id": user.id, "email": user.email, "name": user.name, "avatar": avatar})

# Facebook OAuth
@router.get("/auth/facebook")
def facebook_login():
    params = {
        "client_id": FACEBOOK_CLIENT_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "scope": "email,public_profile",
        "response_type": "code",
        "auth_type": "rerequest"
    }
    url = f"https://www.facebook.com/v12.0/dialog/oauth?{urlencode(params)}"
    return RedirectResponse(url)


@router.get("/auth/facebook/callback")
def facebook_callback(request: Request, code: str = None, db: Session = Depends(get_db)):
    import json
    def popup_response(success, user=None, error=None):
        if success:
            payload = {"type": "oauth-success", "user": user}
        else:
            payload = {"type": "oauth-error", "error": error}
        return (
            f"""
            <html><body><script>
            window.opener && window.opener.postMessage({json.dumps(payload)}, window.origin);
            window.close();
            </script></body></html>
            """
        )
    if not code:
        return popup_response(False, error="No code provided")
    token_url = "https://graph.facebook.com/v12.0/oauth/access_token"
    params = {
        "client_id": FACEBOOK_CLIENT_ID,
        "redirect_uri": FACEBOOK_REDIRECT_URI,
        "client_secret": FACEBOOK_CLIENT_SECRET,
        "code": code
    }
    resp = requests.get(token_url, params=params)
    if resp.status_code != 200:
        return popup_response(False, error="Failed to get access token")
    access_token = resp.json().get("access_token")
    userinfo_resp = requests.get(
        "https://graph.facebook.com/me",
        params={"fields": "id,name,email,picture", "access_token": access_token}
    )
    if userinfo_resp.status_code != 200:
        return popup_response(False, error="Failed to fetch user info from Facebook")
    profile = userinfo_resp.json()
    email = profile.get("email", f"fb_{profile['id']}@facebook.com")
    name = profile.get("name", "")
    avatar = profile.get("picture", {}).get("data", {}).get("url", "")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    return popup_response(True, user={"user_id": user.id, "email": user.email, "name": user.name, "avatar": avatar})

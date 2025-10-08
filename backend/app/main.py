# --- Standard Library Imports ---
import os
import json
import pathlib
from typing import List

# --- Third-Party Imports ---
import requests
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- Project Imports ---
from backend.app import models, schemas, database, crud
from backend.app.database import get_db
from backend.app.schemas import (
    BulletRewriteRequest, BulletRewriteResponse,
    JobPreferences, JobPreferencesCreate, Skill, SkillCreate,
    Education, EducationCreate
)
from backend.app.ai_bullet_rewriter import rewrite_bullet_with_openai
from backend.app.crud_bullet import create_rewritten_bullet
from backend.app.api.auth import router as auth_router
from backend.app.api.user import router as user_router
from backend.app.linkedin_oauth import router as linkedin_router
from backend.app.oauth_providers import router as oauth_router
from backend.app.api.keyword_extraction import router as keyword_extraction_router
from backend.app.api.tailor_resume import router as tailor_resume_router
from backend.app.api.style_tips import router as style_tips_router
from backend.api.suggest_verbs import router as suggest_verbs_router
from backend.api.compare_skills import router as compare_skills_router
from backend.app.resume_export import router as resume_export_router
from backend.api.scan_resume import scan_resume_bp
from backend.app.api.resume import router as resume_router


# --- FastAPI App Setup ---
app = FastAPI(title="Knock-Em-Dead API")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(keyword_extraction_router)
app.include_router(tailor_resume_router)
app.include_router(style_tips_router)
app.include_router(suggest_verbs_router)
app.include_router(compare_skills_router)
app.include_router(linkedin_router)
app.include_router(oauth_router)
app.include_router(resume_export_router)
app.include_router(resume_router)


# --- React Frontend Integration ---
frontend_dir = pathlib.Path(__file__).resolve().parent.parent / "static"
index_file = frontend_dir / "index.html"

if frontend_dir.exists() and index_file.exists():
    # Serve asset subfolder (Vite puts JS/CSS in /assets)
    assets_dir = frontend_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    # Serve top-level static files (favicon, manifest, etc.)
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_root():
        """Serve React root index.html"""
        return FileResponse(index_file)

    @app.exception_handler(404)
    async def spa_fallback(request: Request, exc):
        """
        Serve index.html for SPA routes (React Router) but
        return real 404s for missing static or API paths.
        """
        path = request.url.path
        if (
            request.method == "GET"
            and not path.startswith("/api")
            and "." not in os.path.basename(path)
        ):
            return FileResponse(index_file)
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
else:
    @app.get("/", include_in_schema=False)
    async def serve_health_check():
        """Fallback if no frontend build exists."""
        return {"message": "API is running (no frontend build found)"}


# --- Health Check ---
@app.get("/api/health", include_in_schema=False)
async def health():
    return {"status": "ok"}


# --- Example Endpoint ---
@app.post("/rewrite_bullet", response_model=BulletRewriteResponse)
def rewrite_bullet_endpoint(payload: BulletRewriteRequest, db: Session = Depends(get_db)):
    bullets = rewrite_bullet_with_openai(payload.text)
    for b in bullets:
        create_rewritten_bullet(
            db, original_bullet=payload.text, rewritten_bullet=b, user_id=None
        )
    return BulletRewriteResponse(bullets=bullets)


# --- App Factory ---
def create_app():
    return app


from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import SessionLocal
from ..ai_bullet_rewriter import extract_keywords_with_openai
from backend.app.utils import normalize_keywords
from .. import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class KeywordExtractionRequest(BaseModel):
    job_description: str

class KeywordExtractionResponse(BaseModel):
    keywords: list[str]

@router.post("/extract_keywords", response_model=KeywordExtractionResponse, status_code=status.HTTP_200_OK)
def extract_keywords_endpoint(
    req: KeywordExtractionRequest = Body(...),
    db: Session = Depends(get_db)
):
    raw_keywords = extract_keywords_with_openai(req.job_description)
    keywords = normalize_keywords(raw_keywords)
    return KeywordExtractionResponse(keywords=keywords)

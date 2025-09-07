from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import os
import openai

router = APIRouter()

class SuggestVerbsRequest(BaseModel):
    bullet: str

class SuggestVerbsResponse(BaseModel):
    original: str
    suggestions: List[str]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@router.post("/suggest_verbs", response_model=SuggestVerbsResponse)
def suggest_verbs(request: SuggestVerbsRequest):
    bullet = request.bullet.strip()
    if not bullet:
        raise HTTPException(status_code=400, detail="Bullet cannot be empty.")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured.")

    prompt = (
        "Rewrite this resume bullet with stronger, results-driven action verbs. "
        "Provide 2–3 alternatives. Keep it concise, achievement-oriented, and ATS-friendly. "
        "Return as a JSON array.\n\n"
        f"Bullet: {bullet}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7,
        )
        suggestions = []
        for choice in response.choices:
            try:
                # Try to parse the JSON array from the response
                import json
                suggestions = json.loads(choice.message["content"])
                if isinstance(suggestions, list):
                    break
            except Exception:
                continue
        if not suggestions or not isinstance(suggestions, list):
            raise Exception("Could not parse suggestions from OpenAI response.")
        return SuggestVerbsResponse(original=bullet, suggestions=suggestions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

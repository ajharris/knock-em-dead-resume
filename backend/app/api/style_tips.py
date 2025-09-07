import os
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from .style_tips_schema import StyleTipsRequest, StyleTipsResponse, StyleTip
from typing import List

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@router.post("/style_tips", response_model=StyleTipsResponse)
def get_style_tips(request: StyleTipsRequest):
    resume_text = request.resume_text.strip()
    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")

    prompt = (
        "Analyze this resume content. Return 3–5 style and formatting tips that improve clarity, ATS-readiness, and professionalism. "
        "Output JSON array with fields: tip, severity (one of info, warning, critical).\nResume content:\n" + resume_text
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3,
        )
        # Extract JSON from response
        import json
        import re
        content = response.choices[0].message.content
        # Find JSON array in content
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if not match:
            raise ValueError("No JSON array found in OpenAI response.")
        tips_json = json.loads(match.group(0))
        tips: List[StyleTip] = [StyleTip(**tip) for tip in tips_json]
        return StyleTipsResponse(tips=tips)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

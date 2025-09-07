from pydantic import BaseModel, Field
from typing import List, Literal

class StyleTip(BaseModel):
    tip: str
    severity: Literal['info', 'warning', 'critical']

class StyleTipsRequest(BaseModel):
    resume_text: str = Field(..., example="Experienced software engineer ...")

class StyleTipsResponse(BaseModel):
    tips: List[StyleTip]

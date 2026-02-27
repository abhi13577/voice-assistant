from pydantic import BaseModel, Field
from typing import Optional, Dict


class VoiceRequest(BaseModel):
    transcript: str = Field(..., min_length=1, max_length=1000)
    user_id: int
    project_id: int
    conversation_id: Optional[str] = None
    context_summary: Optional[Dict] = None
from pydantic import BaseModel
from typing import List, Dict, Optional


class SuggestedAction(BaseModel):
    label: str
    action_type: str
    params: Dict


class VoiceResponse(BaseModel):
    intent: str
    escalate: bool
    reply_text: str
    suggested_actions: List[SuggestedAction]
    context_used: List[str]
    confidence: float
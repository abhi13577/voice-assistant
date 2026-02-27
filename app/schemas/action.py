from pydantic import BaseModel
from typing import Dict, Optional


class ActionRequest(BaseModel):
    action_type: str
    params: Dict


class ActionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None
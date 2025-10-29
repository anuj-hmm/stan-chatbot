from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    memory_used: bool = False
from pydantic import BaseModel
from typing import List, Optional

class GenerateResponse(BaseModel):
    source: str
    destination: str
    duration: int
    path: List[str]
    subject: str
    study_plan: Optional[str] = None
    is_too_short: bool = False
    message: Optional[str] = None

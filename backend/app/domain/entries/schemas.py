from datetime import datetime
from pydantic import BaseModel, Field

class EntryCreate(BaseModel):
    entry_text: str | None = None
    
class EntryOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    
    entry_text: str | None
    
    status: str
    error: str | None
    
    valence: float | None
    arousal: float | None
    emotions: dict | None
    evidence: list[str] | None
    
    class config:
        from_attributes = True
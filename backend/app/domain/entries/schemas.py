from datetime import datetime
from pydantic import BaseModel, ConfigDict

class EntryCreate(BaseModel):
    entry_text: str | None = None
    
class EntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    entry_text: str | None = None

    status: str
    error: str | None = None

    valence: float | None = None
    arousal: float | None = None
    emotions: dict | None = None
    evidence: list[str] | None = None
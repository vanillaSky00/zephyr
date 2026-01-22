from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db
from app.domain.entries import repo as entries_repo

router = APIRouter(prefix="/timeline", tags=["timeline"])

class CreateEntryRequest(BaseModel):
    entry_text: str | None = None

@router.post("/")
def create_entry(request: CreateEntryRequest, db: Session = Depends(get_db)):
    # TODO: remove hardcoded user_id
    entry = entries_repo.create_entry(db, user_id=1, entry_text=request.entry_text)
    return {"entry_id": entry.id}
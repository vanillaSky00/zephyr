from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db
from app.domain.entries.schemas import EntryOut
from app.domain.entries import repo as entries_repo

router = APIRouter(prefix="/timeline", tags=["timeline"])

class CreateEntryRequest(BaseModel):
    entry_text: str | None = None

@router.post("/")
def create_entry(request: CreateEntryRequest, db: Session = Depends(get_db)):
    # TODO: remove hardcoded user_id
    entry = entries_repo.create_entry(db, user_id=1, entry_text=request.entry_text)
    return {"entry_id": entry.id}

@router.get("/{entry_id}", response_model=EntryOut)
def get_entry(entry_id: int, db: Session = Depends(get_db), user_id: int = 1):
    e = entries_repo.get_entry_for_user(db, entry_id=entry_id, user_id=user_id)
    if not e:
        raise HTTPException(status_code=404, detail="Entry not found")
    return e
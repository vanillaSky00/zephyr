from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.domain.entries import repo as entries_repo

router = APIRouter(prefix="/timeline", tags=["timeline"])

@router.post("/")
def create_entry(db: Session = Depends(get_db)):
    entry = entries_repo.create_entry(db)
    return {"entry_id": entry.id}
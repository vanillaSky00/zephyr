from sqlalchemy.orm import Session
from app.domain.entries.models import Entry

"""The is an abstraction layer to interact with db. 
   The interaction is related to micro-log and analysis of emotion according to logs
"""

def create_entry(
    db: Session, 
    *, 
    user_id: int,
    entry_text: str | None
) -> Entry:
    e = Entry(user_id=user_id, entry_text=entry_text)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

def get_entry(
    db: Session, 
    *,
    entry_id: int,
    user_id: int
) -> Entry:
    return db.query(Entry) \
             .filter(Entry.id == entry_id, Entry.user_id == user_id) \
             .one()

def set_entry_status(
    db: Session,
    *,
    entry_id: int,
    status: str,
    error: str | None = None
) -> None:
    db.query(Entry) \
      .filter(Entry.id == entry_id) \
      .update({"status": status, "error": error})
    db.commit()

def update_entry_analysis(
    db: Session,
    *,
    entry_id: int,
    valence: float,
    arousal: float,
    emotions: dict,
    evidence: list[str],
    status: str
) -> None:
    db.query(Entry).filter(Entry.id == entry_id) \
      .update(
          {
            "valence": valence,
            "arousal": arousal,
            "emotions": emotions,
            "evidence": evidence,
            "status": status,
            "error": None,
          }
      )
    db.commit()
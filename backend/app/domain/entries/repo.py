from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.entries.models import Entry


def create_entry(
    db: Session,
    *,
    user_id: int,
    entry_text: str | None,
) -> Entry:
    e = Entry(user_id=user_id, entry_text=entry_text)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


# for API: enforce ownership
def get_entry_for_user(
    db: Session,
    *,
    entry_id: int,
    user_id: int,
) -> Entry | None:
    stmt = select(Entry).where(Entry.id == entry_id, Entry.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


# for worker: fetch by PK only
def get_entry_by_id(
    db: Session,
    *,
    entry_id: int,
) -> Entry | None:
    stmt = select(Entry).where(Entry.id == entry_id)
    return db.execute(stmt).scalar_one_or_none()


def set_entry_status(
    db: Session,
    *,
    entry_id: int,
    status: str,
    error: str | None = None,
) -> None:
    # (optional) could also fetch and set fields, but update is fine
    db.query(Entry).filter(Entry.id == entry_id).update(
        {"status": status, "error": error}
    )
    db.commit()


def update_entry_analysis(
    db: Session,
    *,
    entry_id: int,
    valence: float,
    arousal: float,
    emotions: dict,
    evidence: list[str],
    status: str,
) -> None:
    db.query(Entry).filter(Entry.id == entry_id).update(
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

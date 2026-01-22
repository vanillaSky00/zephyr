from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.common.enums import JobStatus, MediaType
from app.domain.entries import repo as entry_repo
from app.domain.entries.models import Entry
from app.domain.media.models import Media
from app.infrastructure.ml.emotion import infer

def analyze_entry_job(entry_id: int) -> None:
    db: Session = SessionLocal()
    try:
        entry_repo.set_entry_status(db, entry_id=entry_id, status=JobStatus.RUNNING)

        entry: Entry = db.query(Entry).filter(Entry.id == entry_id).one()
        voices: list[Media] = (
            db.query(Media)
            .filter(Media.entry_id == entry_id, Media.type == MediaType.VOICE, Media.status == JobStatus.DONE)
            .all()
        )

        transcript = " ".join(v.transcript for v in voices if v.transcript)
        base = (entry.entry_text or "").strip()
        text = (base + "\n" + transcript).strip() if transcript else base

        if not text:
            entry_repo.set_entry_status(db, entry_id=entry_id, status=JobStatus.FAILED, error="No text to analyze.")
            return

        valence, arousal, emotions, evidence = infer(text)
        entry_repo.update_entry_analysis(
            db,
            entry_id=entry_id,
            valence=valence,
            arousal=arousal,
            emotions=emotions,
            evidence=evidence,
            status=JobStatus.DONE,
        )
    except Exception as e:
        entry_repo.set_entry_status(db, entry_id=entry_id, status=JobStatus.FAILED, error=str(e))
        raise
    finally:
        db.close()

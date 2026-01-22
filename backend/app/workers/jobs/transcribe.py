from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.common.enums import JobStatus
from app.domain.media import repo as media_repo
from app.infrastructure.ml.whisper import transcribe
from app.infrastructure.queue.rq import enqueue
from app.workers.jobs.analyze import analyze_entry_job

def transcribe_voice_job(media_id: int) -> None:
    db: Session = SessionLocal()
    try:
        media_repo.set_media_status(db, media_id=media_id, status=JobStatus.RUNNING)

        m = media_repo.get_media(db, media_id=media_id)
        text, lang = transcribe(m.storage_path)

        media_repo.set_transcript(db, media_id=media_id, transcript=text, lang=lang, status=JobStatus.DONE)

        # chain analyze
        enqueue(analyze_entry_job, m.entry_id)

    except Exception as e:
        media_repo.set_media_status(db, media_id=media_id, status=JobStatus.FAILED, error=str(e))
        raise
    finally:
        db.close()

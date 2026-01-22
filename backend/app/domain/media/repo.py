from sqlalchemy.orm import Session
from app.domain.media.models import Media


def create_video_media(
    db: Session, 
    *, 
    entry_id: int,
    storage_path: str 
) -> Media:
    m = Media(entry_id=entry_id, type="voice", storage_path=storage_path)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def get_media(
    db: Session, 
    *,
    media_id: int,
) -> Media:
    return db.query(Media) \
             .filter(Media.id == media_id) \
             .one()

def set_media_status(
    db: Session,
    *,
    media_id: int,
    status: str,
    error: str | None = None
) -> None:
    db.query(Media) \
      .filter(Media.id == media_id) \
      .update({"status", status, "error", error})
    db.commit()

def set_transcript(
    db: Session,
    *,
    media_id: int,
    transcript: str,
    lang: str | None,
    status: str
) -> None:
    db.query(Media) \
      .filter(Media.id == media_id) \
      .update(
          {
            "transcript": transcript,
            "lang": lang,
            "status": status,
            "error": None,
          }
      ) 
    db.commit()
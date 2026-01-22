from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.infrastructure.storage.local import save_upload
from app.domain.media import repo as media_repo
from app.infrastructure.queue.rq import enqueue
from app.workers.jobs.transcribe import transcribe_voice_job

router = APIRouter(prefix="/media", tags=["media"])

@router.post("/voice")
def upload_voice(entry_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = save_upload(file, subdir=f"entry_{entry_id}/voice")
    m = media_repo.create_voice_media(db, entry_id=entry_id, storage_path=path)
    enqueue(transcribe_voice_job, m.id)
    return {"media_id": m.id, "status": m.status}

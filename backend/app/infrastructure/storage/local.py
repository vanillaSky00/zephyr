from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

from app.settings import settings

def save_upload(file: UploadFile, *, subdir: str) -> str:
    base = Path(settings.STORAGE_DIR) / subdir
    base.mkdir(parents=True, exist_ok=True)
    
    suffix = Path(file.filename or "").suffix or ".bin"
    name = f"{uuid4().hex}{suffix}"
    path = base / name
    
    with path.open("wb") as f:
        f.write(file.file.read())
        
    return str(path)
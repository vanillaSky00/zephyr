import subprocess
import tempfile
import os
from faster_whisper import WhisperModel
from app.settings import settings

_model: WhisperModel | None = None

def get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel(
            settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE,
        )
    return _model

def to_wav_16k_mono(input_path: str) -> str:
    temp_wav = tempfile.mkstemp(suffix=".wav")[1]
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", input_path, "-ac", "1", "-ar", "16000", temp_wav],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg failed to convert {input_path} to wav: {e.stderr}") from e
    return temp_wav

def transcribe(path: str) -> tuple[str, str | None]:
    wav_path = to_wav_16k_mono(path)
    try:
        model = get_model()
        segments, info = model.transcribe(wav_path)
        text = " ".join(s.text.strip() for s in segments).strip()
        lang = getattr(info, "language", None)
        return text, lang
    finally:
        os.remove(wav_path)

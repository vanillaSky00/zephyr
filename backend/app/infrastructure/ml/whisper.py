import subprocess
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
    out = input_path + ".wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-ac", "1", "-ar", "16000", out],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return out

def transcribe(path: str) -> tuple[str, str | None]:
    wav = to_wav_16k_mono(path)
    model = get_model()
    segments, info = model.transcribe(wav)
    text = " ".join(s.text.strip() for s in segments).strip()
    lang = getattr(info, "language", None)
    return text, lang

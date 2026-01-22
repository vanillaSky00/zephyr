import re
from transformers import pipeline
from app.settings import settings

_pipe = None

VALENCE_MAP = {
    "joy": 0.8,
    "sadness": -0.7,
    "anger": -0.8,
    "fear": -0.6,
    "surprise": 0.1,
    "disgust": -0.6,
    "neutral": 0.0,
}

def get_pipe():
    global _pipe
    if _pipe is None:
        _pipe = pipeline("text-classification", model=settings.EMOTION_MODEL, top_k=5)
    return _pipe

def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]

def infer(text: str) -> tuple[float, float, dict, list[str]]:
    pipe = get_pipe()
    preds = pipe(text)[0]
    top = [{"label": p["label"].lower(), "score": float(p["score"])} for p in preds]

    # valence
    num = 0.0
    den = 0.0
    for t in top:
        if t["label"] in VALENCE_MAP:
            num += VALENCE_MAP[t["label"]] * t["score"]
            den += t["score"]
    valence = num / den if den else 0.0

    # arousal heuristic MVP
    arousal = min(
        1.0,
        0.15
        + 0.08 * sum(ch in "!?." for ch in text)
        + 0.04 * sum(w.isupper() for w in text.split()),
    )

    # evidence
    top_label = top[0]["label"] if top else "neutral"
    sents = split_sentences(text)[:30]
    scored = []
    for s in sents:
        sp = pipe(s)[0]
        sp_map = {x["label"].lower(): float(x["score"]) for x in sp}
        scored.append((sp_map.get(top_label, 0.0), s))
    scored.sort(reverse=True, key=lambda x: x[0])
    evidence = [s for _, s in scored[:3]]

    return float(valence), float(arousal), {"top": top}, evidence

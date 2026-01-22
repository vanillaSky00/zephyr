from collections import defaultdict
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.domain.entries.models import Entry
from app.common.enums import JobStatus

def daily_timeline(db: Session, *, user_id: int, date_from: date, date_to: date) -> list[dict]:
    # Fetch done entries in range (inclusive)
    rows = (
        db.query(Entry)
        .filter(
            Entry.user_id == user_id,
            Entry.status == JobStatus.DONE,
            func.date(Entry.created_at) >= date_from,
            func.date(Entry.created_at) <= date_to,
        )
        .all()
    )

    by_day: dict[date, list[Entry]] = defaultdict(list)
    for r in rows:
        by_day[r.created_at.date()].append(r)

    out: list[dict] = []
    for d in sorted(by_day.keys()):
        items = by_day[d]
        val = [x.valence for x in items if x.valence is not None]
        aro = [x.arousal for x in items if x.arousal is not None]

        # Aggregate emotions: sum scores for each label if present
        emo_sum: dict[str, float] = defaultdict(float)
        for x in items:
            top = (x.emotions or {}).get("top", [])
            for t in top:
                emo_sum[t["label"]] += float(t["score"])

        top_emotions = sorted(
            [{"label": k, "score": v} for k, v in emo_sum.items()],
            key=lambda a: a["score"],
            reverse=True,
        )[:5]

        out.append(
            {
                "date": d.isoformat(),
                "valence_avg": (sum(val) / len(val)) if val else None,
                "arousal_avg": (sum(aro) / len(aro)) if aro else None,
                "top_emotions": top_emotions,
                "count": len(items),
            }
        )
    return out

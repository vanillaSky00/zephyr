from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Float, JSON, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import JobStatus
from app.infrastructure.db.base import Base
class Entry(Base):
    __tablename__ = "entries"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        index=True
    )
    
    entry_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    status: Mapped[str] = mapped_column(String(16), default=JobStatus.PENDING, index=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    valence: Mapped[Float | None] = mapped_column(Float, nullable=True) 
    arousal: Mapped[Float | None] = mapped_column(Float, nullable=True) 
    emotions: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # {"top":[...]}
    evidence: Mapped[list | None] = mapped_column(JSON, nullable=True)  # list[str]
    
    media = relationship("Media", back_populates="entry", cascade="all, delete-orphan")
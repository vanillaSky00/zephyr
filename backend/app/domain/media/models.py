from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base
from app.common.enums import JobStatus, MediaType

class Media(Base):
    __tablename__ = "media"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_id: Mapped[int] = mapped_column(
        ForeignKey("entries.id", ondelete="CASCADE"),
        index=True,
    )
    type: Mapped[str] = mapped_column(String(16), default=MediaType.VOICE)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    storage_path: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(16),
        default=JobStatus.PENDING,
        index=True
    )
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    lang: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    entry = relationship("Entry", back_populates="media")
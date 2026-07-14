from datetime import datetime

from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.opportunity import Opportunity
    from app.models.source import Information


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    information_id: Mapped[int] = mapped_column(
        ForeignKey("information.id"), unique=True, nullable=False, index=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    key_topics: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    commercial_potential: Mapped[str] = mapped_column(String(20), nullable=False, default="unknown")
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    raw_response: Mapped[dict | None] = mapped_column(JSONB)

    information: Mapped["Information"] = relationship(back_populates="analysis")
    opportunity: Mapped["Opportunity | None"] = relationship(back_populates="analysis", uselist=False)

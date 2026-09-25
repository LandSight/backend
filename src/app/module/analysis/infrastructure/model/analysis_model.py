"""SQLAlchemy ORM model for Analysis."""

import datetime  # noqa: TC003
from uuid import UUID  # noqa: TC003

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class AnalysisModel(TimestampedModel):
    """ORM model for the Analysis entity.

    Maps to the ``analysis.analyses`` table.
    """

    __tablename__ = "analyses"
    __table_args__ = {"schema": "analysis"}  # noqa: RUF012

    parcel_id: Mapped[UUID] = mapped_column(
        ForeignKey("parcel.parcels.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the parcel being analysed",
    )
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Human-readable analysis name",
    )
    analysis_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Evaluation profile (e.g. izhs)",
    )
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="Lifecycle status (pending/running/completed/failed)",
    )
    stage: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="Pipeline stage (metrics/scoring)",
    )
    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Final score in [0, 10]; NULL until completed",
    )
    model_version: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="Version of the scoring model; NULL until completed",
    )
    status_reason: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="Human-readable status explanation",
    )
    completed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the analysis completed (UTC); NULL until completed",
    )


__all__ = ("AnalysisModel",)

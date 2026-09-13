"""SQLAlchemy ORM model for Analysis."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, String
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
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="Lifecycle status (pending/running/completed/failed)",
    )
    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Final score in [0, 10]; NULL until completed",
    )
    status_reason: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="Human-readable status explanation",
    )


__all__ = ("AnalysisModel",)

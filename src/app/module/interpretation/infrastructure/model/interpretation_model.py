"""SQLAlchemy ORM model for a stored interpretation report."""

from __future__ import annotations

from uuid import UUID  # noqa: TC003

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class InterpretationModel(TimestampedModel):
    """ORM model for one interpretation report.

    A report belongs to exactly one analysis and stores only the generated text
    and the model that produced it; scores and evaluation metadata are not
    duplicated and are recomputed from the current evaluation when the report is
    read. Maps to the ``interpretation.interpretations`` table.
    """

    __tablename__ = "interpretations"
    __table_args__ = (
        Index("ix_interpretations_analysis_id", "analysis_id", unique=True),
        {"schema": "interpretation"},
    )

    analysis_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analyses.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the analysis the report belongs to",
    )
    model: Mapped[str] = mapped_column(String(128), nullable=False, comment="Model that generated the report")
    summary: Mapped[str] = mapped_column(Text, nullable=False, comment="Combined top-aspects summary")
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default="completed",
        comment="Report generation status: ordered/running/completed/failed/cancelled",
    )
    attempt_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        default=None,
        comment="Generation attempt that owns the running report",
    )
    progress_done: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Texts generated so far by the running attempt",
    )
    progress_total: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
        comment="Texts the running attempt has to generate",
    )
    constraints_explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        server_default="",
        comment="Explanation of the restriction zones that lowered the score",
    )
    aspect_explanations: Mapped[dict[str, str]] = mapped_column(
        JSONB,
        nullable=False,
        default_factory=dict,
        comment="Explanation text keyed by aspect key",
    )


__all__ = ("InterpretationModel",)

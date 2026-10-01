"""SQLAlchemy ORM model for a stored interpretation report."""

from __future__ import annotations

from uuid import UUID  # noqa: TC003

from sqlalchemy import ForeignKey, Index, String, Text
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
    aspect_explanations: Mapped[dict[str, str]] = mapped_column(
        JSONB,
        nullable=False,
        default_factory=dict,
        comment="Explanation text keyed by aspect key",
    )


__all__ = ("InterpretationModel",)

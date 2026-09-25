"""SQLAlchemy ORM model for an analysis evaluation."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class AnalysisEvaluationModel(TimestampedModel):
    """ORM model for the AnalysisEvaluation aggregate root.

    Maps to the ``analysis.analysis_evaluations`` table.
    """

    __tablename__ = "analysis_evaluations"
    __table_args__ = (
        Index("ix_analysis_evaluations_analysis_id", "analysis_id"),
        {"schema": "analysis"},
    )

    analysis_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analyses.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the owning analysis",
    )
    analysis_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Evaluation profile (e.g. izhs)",
    )
    model_version: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Version of the hierarchy and normalization configuration used",
    )
    total_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Final score on the 0-10 scale",
    )


__all__ = ("AnalysisEvaluationModel",)

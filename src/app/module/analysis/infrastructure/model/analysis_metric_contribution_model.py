"""SQLAlchemy ORM model for a metric contribution of an evaluation."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class AnalysisMetricContributionModel(BaseModel):
    """ORM model for one metric contribution in an analysis evaluation.

    Maps to the ``analysis.analysis_metric_contributions`` table.
    """

    __tablename__ = "analysis_metric_contributions"
    __table_args__ = (
        Index("ix_analysis_metric_contributions_evaluation_id", "evaluation_id"),
        Index("ix_analysis_metric_contributions_cluster_score_id", "cluster_score_id"),
        {"schema": "analysis"},
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analysis_evaluations.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the owning evaluation",
    )
    cluster_score_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analysis_cluster_scores.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the group this metric belongs to",
    )
    metric_key: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Metric key",
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Display order within its group",
    )
    raw_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Raw metric reading; NULL when unavailable",
    )
    normalized_value: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Normalized value in [0, 1]; NULL when unavailable",
    )
    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Configured weight among siblings",
    )
    contribution: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="normalized_value * weight",
    )
    unit: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Unit of the raw value",
    )
    membership_function: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="Name of the applied membership function",
    )
    membership_params: Mapped[dict[str, float] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Parameters of the applied membership function",
    )


__all__ = ("AnalysisMetricContributionModel",)

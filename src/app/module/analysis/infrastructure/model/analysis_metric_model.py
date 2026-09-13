"""SQLAlchemy ORM model linking an Analysis to the metrics it used."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class AnalysisMetricModel(BaseModel):
    """ORM model for the analysis-metrics link.

    Maps to the ``analysis.analysis_metrics`` table. ``metric_id`` is a weak
    reference into another module's metrics snapshot, so it intentionally has no
    database-level foreign key.
    """

    __tablename__ = "analysis_metrics"
    __table_args__ = (
        Index("ix_analysis_metrics_analysis_id", "analysis_id"),
        {"schema": "analysis"},
    )

    analysis_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analyses.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the owning analysis",
    )
    metric_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Metric module (topography/climate/infrastructure)",
    )
    category: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        comment="Infrastructure category; NULL for single-metric modules",
    )
    metric_id: Mapped[UUID] = mapped_column(
        nullable=False,
        comment="ID of the referenced metrics snapshot",
    )


__all__ = ("AnalysisMetricModel",)

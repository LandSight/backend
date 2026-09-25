"""SQLAlchemy ORM model for a cluster (group) evaluation score."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class AnalysisClusterScoreModel(BaseModel):
    """ORM model for a group score of an analysis evaluation.

    The same table stores top-level clusters and nested subclusters: a row with
    ``parent_id`` is a subcluster of the row it points to. Maps to the
    ``analysis.analysis_cluster_scores`` table.
    """

    __tablename__ = "analysis_cluster_scores"
    __table_args__ = (
        Index("ix_analysis_cluster_scores_evaluation_id", "evaluation_id"),
        Index("ix_analysis_cluster_scores_parent_id", "parent_id"),
        {"schema": "analysis"},
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analysis_evaluations.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the owning evaluation",
    )
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("analysis.analysis_cluster_scores.id", ondelete="CASCADE"),
        nullable=True,
        comment="ID of the parent group; NULL for a top-level cluster",
    )
    key: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Group key (e.g. relief or slope)",
    )
    depth: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Nesting depth; 0 for a top-level cluster",
    )
    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Aggregated group score in [0, 1]",
    )
    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Configured group weight",
    )
    contribution: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="score * weight",
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Display order within the parent",
    )


__all__ = ("AnalysisClusterScoreModel",)

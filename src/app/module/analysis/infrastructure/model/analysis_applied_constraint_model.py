"""SQLAlchemy ORM model for a constraint applied to an analysis evaluation."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class AnalysisAppliedConstraintModel(BaseModel):
    """ORM model for an AppliedConstraint of an evaluation.

    Maps to the ``analysis.analysis_applied_constraints`` table.
    """

    __tablename__ = "analysis_applied_constraints"
    __table_args__ = (
        Index("ix_analysis_applied_constraints_evaluation_id", "evaluation_id"),
        {"schema": "analysis"},
    )

    evaluation_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analysis_evaluations.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the owning evaluation",
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Order of the constraint within the evaluation",
    )
    kind: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Restriction zone kind",
    )
    effect: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="prohibit or penalty",
    )
    factor: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Multiplier applied to the score",
    )
    overlap_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Share of the parcel inside the zone, 0..1",
    )
    overlap_area_m2: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Area of the parcel inside the zone in square meters",
    )
    zone_names: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        comment="Names of the source objects, when known",
    )
    legal_basis: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Short reference to the rule that defines the zone",
    )


__all__ = ("AnalysisAppliedConstraintModel",)

"""SQLAlchemy ORM model linking an Analysis to its restriction check."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import UUID as SA_UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class AnalysisRestrictionCheckModel(BaseModel):
    """ORM model for the analysis-restriction check link.

    Maps to the ``analysis.analysis_restriction_checks`` table; one check per
    analysis. ``check_id`` is a weak reference into the restriction module's
    snapshot, so it intentionally has no database-level foreign key.
    """

    __tablename__ = "analysis_restriction_checks"
    __table_args__ = {"schema": "analysis"}  # noqa: RUF012

    analysis_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis.analyses.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        comment="ID of the owning analysis",
    )
    check_id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        nullable=False,
        comment="ID of the restriction check snapshot (weak reference)",
    )


__all__ = ("AnalysisRestrictionCheckModel",)

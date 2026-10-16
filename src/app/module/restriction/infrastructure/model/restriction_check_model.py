"""SQLAlchemy ORM model for restriction checks."""

from __future__ import annotations

from uuid import UUID  # noqa: TC003

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class RestrictionCheckModel(TimestampedModel):
    """ORM model for the RestrictionCheck entity.

    Maps to the ``restriction.checks`` table. Append-only: every check is a
    new snapshot so analyses keep referencing the exact zones they were
    scored with.
    """

    __tablename__ = "checks"
    __table_args__ = {"schema": "restriction"}  # noqa: RUF012

    parcel_id: Mapped[UUID] = mapped_column(
        ForeignKey("parcel.parcels.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the checked parcel",
    )
    rules_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Version of the zone rules the zones were built with",
    )


__all__ = ("RestrictionCheckModel",)

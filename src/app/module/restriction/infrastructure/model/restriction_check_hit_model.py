"""SQLAlchemy ORM model for restriction check hits."""

from __future__ import annotations

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class RestrictionCheckHitModel(BaseModel):
    """ORM model for one overlapping zone kind of a restriction check.

    Maps to the ``restriction.check_hits`` table.
    """

    __tablename__ = "check_hits"
    __table_args__ = {"schema": "restriction"}  # noqa: RUF012

    check_id: Mapped[UUID] = mapped_column(
        ForeignKey("restriction.checks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID of the restriction check",
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Order of the hit within the check",
    )
    kind: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Zone kind, see RestrictionKind",
    )
    overlap_area_m2: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Area of the parcel inside the zones in square meters",
    )
    overlap_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Share of the parcel area inside the zones, 0..1",
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


__all__ = ("RestrictionCheckHitModel",)

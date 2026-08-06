"""SQLAlchemy ORM model for SchoolMetrics."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


if TYPE_CHECKING:
    from uuid import UUID


class SchoolMetricsModel(TimestampedModel):
    """ORM model for the SchoolMetrics entity.

    Maps to the ``infrastructure.parcel_school_metrics`` table.
    """

    __tablename__ = "parcel_school_metrics"
    __table_args__ = {"schema": "infrastructure"}  # noqa: RUF012

    parcel_id: Mapped[UUID] = mapped_column(
        ForeignKey("parcel.parcels.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the parcel these metrics belong to",
    )
    buffer: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Buffer radius in meters around the parcel boundary",
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Number of school objects within the buffer",
    )
    min_distance_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest school in meters, or NULL if none found",
    )


__all__ = ("SchoolMetricsModel",)

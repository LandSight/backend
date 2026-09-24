"""SQLAlchemy ORM model for GeographicPositionMetrics."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class GeographicPositionMetricsModel(TimestampedModel):
    """ORM model for the GeographicPositionMetrics entity.

    Maps to the ``infrastructure.parcel_geographic_position_metrics`` table.
    """

    __tablename__ = "parcel_geographic_position_metrics"
    __table_args__ = {"schema": "infrastructure"}  # noqa: RUF012

    parcel_id: Mapped[UUID] = mapped_column(
        ForeignKey("parcel.parcels.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the parcel these metrics belong to",
    )
    buffer: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Search radius in meters around the parcel boundary",
    )
    distance_to_regional_center: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest regional center in meters, or NULL if none found",
    )
    distance_to_district_center: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest district center in meters, or NULL if none found",
    )
    distance_to_settlement: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest local settlement in meters, or NULL if none found",
    )


__all__ = ("GeographicPositionMetricsModel",)

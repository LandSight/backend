"""SQLAlchemy ORM model for GeographicPositionMetrics."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer, Text
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
    distance_to_major_city: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest major city in meters, or NULL if none found",
    )
    city_tier: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Tier of the nearest major city (regional_center, district_center, local_town, unknown)",
    )


__all__ = ("GeographicPositionMetricsModel",)

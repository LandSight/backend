"""SQLAlchemy ORM model for RoadAccessibilityMetrics."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class RoadAccessibilityMetricsModel(TimestampedModel):
    """ORM model for the RoadAccessibilityMetrics entity.

    Maps to the ``infrastructure.parcel_road_accessibility_metrics`` table.
    """

    __tablename__ = "parcel_road_accessibility_metrics"
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
    distance_to_paved_road: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest paved road in meters, or NULL if none found",
    )
    distance_to_main_road: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest main road in meters, or NULL if none found",
    )
    distance_to_any_road: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest drivable road in meters, or NULL if none found",
    )
    road_density_1km: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Road network density within the buffer in km/km2",
    )


__all__ = ("RoadAccessibilityMetricsModel",)

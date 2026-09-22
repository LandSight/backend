"""SQLAlchemy ORM model for UtilityMetrics."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class UtilityMetricsModel(TimestampedModel):
    """ORM model for the UtilityMetrics entity.

    Maps to the ``infrastructure.parcel_utility_metrics`` table and holds power
    lines, gas pipelines and water pipelines, disambiguated by ``utility_type``.
    """

    __tablename__ = "parcel_utility_metrics"
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
    utility_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Utility category (power_line, gas_pipeline, water_pipeline)",
    )
    min_distance_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest utility network in meters, or NULL if none found",
    )


__all__ = ("UtilityMetricsModel",)

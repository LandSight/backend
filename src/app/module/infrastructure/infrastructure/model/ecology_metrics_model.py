"""SQLAlchemy ORM model for EcologyMetrics."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class EcologyMetricsModel(TimestampedModel):
    """ORM model for the EcologyMetrics entity.

    Maps to the ``infrastructure.parcel_ecology_metrics`` table and holds water
    bodies, forests and protected areas, disambiguated by ``object_type``.
    """

    __tablename__ = "parcel_ecology_metrics"
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
    object_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Ecology category (water_body, forest, protected_area)",
    )
    coverage_ratio: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Fraction of the buffer zone covered by the objects in [0, 1]",
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Number of distinct (connected) objects within the buffer",
    )
    min_distance_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest object in meters, or NULL if none found",
    )
    distance_to_large_object: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest large object in meters, or NULL if none found",
    )


__all__ = ("EcologyMetricsModel",)

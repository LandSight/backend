"""SQLAlchemy ORM model for FacilityMetrics."""

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class FacilityMetricsModel(TimestampedModel):
    """ORM model for the FacilityMetrics entity.

    Maps to the ``infrastructure.parcel_facility_metrics`` table and holds
    schools, hospitals, grocery shops, bus stops and railway stations,
    disambiguated by ``facility_type``.
    """

    __tablename__ = "parcel_facility_metrics"
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
    facility_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Facility category (school, hospital, grocery, bus_stop, railway_station)",
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Number of facility objects within the buffer",
    )
    min_distance_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest facility in meters, or NULL if none found",
    )


__all__ = ("FacilityMetricsModel",)

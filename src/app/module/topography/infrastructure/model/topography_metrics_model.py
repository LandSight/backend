"""SQLAlchemy ORM model for TopographyMetrics."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


if TYPE_CHECKING:
    from uuid import UUID


class TopographyMetricsModel(TimestampedModel):
    """ORM model for the TopographyMetrics entity.

    Maps to the ``topography.metrics`` table.

    Stores all computed topography metrics as scalar columns,
    with JSONB for complex structures (percentiles, distribution).
    """

    __tablename__ = "metrics"
    __table_args__ = {"schema": "topography"}  # noqa: RUF012

    parcel_id: Mapped[UUID] = mapped_column(
        ForeignKey("parcel.parcels.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the parcel these metrics belong to",
    )
    mean_elevation: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Mean elevation in meters",
    )
    max_elevation: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Maximum elevation in meters",
    )
    min_elevation: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Minimum elevation in meters",
    )
    elevation_range: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Elevation range (max - min) in meters",
    )
    elevation_std: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Standard deviation of elevation in meters",
    )
    mean_slope: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Mean slope in degrees",
    )
    max_slope: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Maximum slope in degrees",
    )
    slope_percentiles: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        comment="Slope values at percentiles 25, 50, 75, 90 as JSON dict",
    )
    slope_distribution: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        comment="Slope histogram bins (10 bins, 0-90°) as JSON array",
    )
    aspect: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        comment="Dominant slope aspect direction (N/NE/E/SE/S/SW/W/NW/FLAT)",
    )
    south_aspect_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Percentage of area facing south (SE, S, SW)",
    )
    area: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Parcel area in square meters",
    )
    perimeter: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Parcel perimeter in meters",
    )
    compactness_index: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Compactness index (4πA/P²), dimensionless",
    )
    elongation_index: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Elongation index (width/length), dimensionless",
    )


__all__ = ("TopographyMetricsModel",)

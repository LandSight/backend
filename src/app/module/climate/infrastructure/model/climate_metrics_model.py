"""SQLAlchemy ORM model for ClimateMetrics."""

from __future__ import annotations

from uuid import UUID  # noqa: TC003

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class ClimateMetricsModel(TimestampedModel):
    """ORM model for the ClimateMetrics entity.

    Maps to the ``climate.metrics`` table.

    Stores all computed climate metrics as scalar columns. Temperature values
    are stored in °C (already converted from the raw WorldClim scaling).
    """

    __tablename__ = "metrics"
    __table_args__ = {"schema": "climate"}  # noqa: RUF012

    parcel_id: Mapped[UUID] = mapped_column(
        ForeignKey("parcel.parcels.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the parcel these metrics belong to",
    )
    mean_annual_temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Mean annual temperature (BIO1) in °C",
    )
    annual_precipitation: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Annual precipitation (BIO12) in mm",
    )
    temperature_seasonality: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Temperature seasonality (BIO4) in °C",
    )
    precipitation_seasonality: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Precipitation seasonality (BIO15), coefficient of variation in %",
    )
    max_temperature_warmest_month: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Max temperature of the warmest month (BIO5) in °C",
    )
    min_temperature_coldest_month: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Min temperature of the coldest month (BIO6) in °C",
    )
    precipitation_wettest_month: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Precipitation of the wettest month (BIO13) in mm",
    )
    precipitation_driest_month: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Precipitation of the driest month (BIO14) in mm",
    )


__all__ = ("ClimateMetricsModel",)

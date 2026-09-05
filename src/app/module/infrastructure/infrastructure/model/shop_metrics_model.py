"""SQLAlchemy ORM model for ShopMetrics."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


if TYPE_CHECKING:
    from uuid import UUID


class ShopMetricsModel(TimestampedModel):
    """ORM model for the ShopMetrics entity.

    Maps to the ``infrastructure.parcel_shop_metrics`` table.
    """

    __tablename__ = "parcel_shop_metrics"
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
        comment="Number of shop objects within the buffer",
    )
    min_distance_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Distance to the nearest shop in meters, or NULL if none found",
    )


__all__ = ("ShopMetricsModel",)

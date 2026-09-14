"""SQLAlchemy ORM model for Parcel."""

from uuid import UUID  # noqa: TC003

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import TimestampedModel


class ParcelModel(TimestampedModel):
    """ORM model for the Parcel entity.

    Maps to the ``parcel.parcels`` table.

    Uses PostGIS ``Geometry(Polygon, 4326)`` for geographic data storage.
    SRID 4326 corresponds to WGS 84 (standard GPS coordinates).
    """

    __tablename__ = "parcels"
    __table_args__ = {"schema": "parcel"}  # noqa: RUF012

    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    polygon: Mapped[Geometry] = mapped_column(
        Geometry("Polygon", srid=4326),
        nullable=False,
        comment="PostGIS Polygon geometry in SRID 4326 (WGS 84)",
    )
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("identity.users.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the user who owns this parcel",
    )


__all__ = ("ParcelModel",)

"""SQLAlchemy ORM model for the OSM polygon layer (``planet_osm_polygon``).

This table is created by ``osm2pgsql`` when importing OpenStreetMap data.
It contains area-based features such as water bodies, buildings and forests.
The model is read-only: the table is populated externally by the OSM import
and is not managed by the application's migrations.
"""

from __future__ import annotations

from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Text
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.database.base import BaseModel


class PlanetOsmPolygonModel(BaseModel):
    """ORM model for the ``planet_osm_polygon`` table.

    Maps to the ``infrastructure.planet_osm_polygon`` table created by ``osm2pgsql``.

    ``way`` stores the polygon geometry in SRID 3857 (Web Mercator), the
    default projection used by ``osm2pgsql``.
    """

    __tablename__ = "planet_osm_polygon"
    __table_args__ = {"schema": "infrastructure"}  # noqa: RUF012

    osm_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="OSM identifier of the feature",
    )
    name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Human-readable name of the feature",
    )
    way: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="POLYGON", srid=3857),
        nullable=False,
        comment="Polygon geometry in SRID 3857 (Web Mercator)",
    )
    tags: Mapped[dict | None] = mapped_column(
        HSTORE,
        nullable=True,
        comment="Key-value tags of the OSM feature",
    )


__all__ = ("PlanetOsmPolygonModel",)

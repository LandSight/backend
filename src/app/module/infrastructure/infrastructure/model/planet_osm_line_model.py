"""SQLAlchemy ORM model for the OSM line layer (``planet_osm_line``).

This table is created by ``osm2pgsql`` when importing OpenStreetMap data.
It contains linear features such as roads, railways, power lines, pipelines and
river centerlines. The model is read-only: the table is populated externally by
the OSM import and is not managed by the application's migrations.
"""

from __future__ import annotations

from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Text
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.orm import Mapped, mapped_column

from app.module.shared.infrastructure.geo import Srid
from app.platform.database.base import BaseModel


class PlanetOsmLineModel(BaseModel):
    """ORM model for the ``planet_osm_line`` table.

    Maps to the ``infrastructure.planet_osm_line`` table created by ``osm2pgsql``.

    ``way`` stores the line geometry in SRID 3857 (Web Mercator), the default
    projection used by ``osm2pgsql``.
    """

    __tablename__ = "planet_osm_line"
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
        Geometry(geometry_type="LINESTRING", srid=Srid.WEB_MERCATOR),
        nullable=False,
        comment="Line geometry in SRID 3857 (Web Mercator)",
    )
    tags: Mapped[dict | None] = mapped_column(
        HSTORE,
        nullable=True,
        comment="Key-value tags of the OSM feature",
    )


__all__ = ("PlanetOsmLineModel",)

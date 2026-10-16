"""SQLAlchemy ORM model for restriction zones."""

from __future__ import annotations

from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import BigInteger, Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.module.shared.infrastructure.geo import Srid
from app.platform.database.base import BaseModel


class ZoneModel(BaseModel):
    """ORM model for a prebuilt restriction zone.

    Maps to the ``restriction.zones`` table. Rows are written by the zone ETL
    (``app.module.restriction.etl.build_osm_zones``) and only read by the
    application. Geometry is kept in Web Mercator, like the OSM layers it is
    built from, so the GIST index serves the intersection test directly.
    """

    __tablename__ = "zones"
    __table_args__ = {"schema": "restriction"}  # noqa: RUF012

    kind: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        comment="Zone kind, see RestrictionKind",
    )
    source_layer: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        comment="OSM layer the zone was built from: point, line or polygon",
    )
    source_osm_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="osm2pgsql osm_id of the source object",
    )
    name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Name of the source object, when tagged",
    )
    legal_basis: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Short reference to the rule that defines the zone",
    )
    width_m: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Buffer width around the source object in meters; 0 for the object itself",
    )
    attributes: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        comment="Source attributes the width was derived from",
    )
    rules_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Hash of the zone rules file the zone was built with",
    )
    geom: Mapped[Geometry] = mapped_column(
        Geometry("MULTIPOLYGON", srid=Srid.WEB_MERCATOR, spatial_index=True),
        nullable=False,
        comment="Zone geometry in SRID 3857 (Web Mercator)",
    )


__all__ = ("ZoneModel",)

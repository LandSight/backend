"""Add restriction zones table.

Zones are prebuilt by the restriction zone ETL from OSM with regulatory
buffers and only read by the application.

Revision ID: d23e62e90475
Revises:
Create Date: 2026-10-12 12:06:23.723750

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "d23e62e90475"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "zones",
        sa.Column("kind", sa.String(length=64), nullable=False, comment="Zone kind, see RestrictionKind"),
        sa.Column(
            "source_layer",
            sa.String(length=16),
            nullable=False,
            comment="OSM layer the zone was built from: point, line or polygon",
        ),
        sa.Column("source_osm_id", sa.BigInteger(), nullable=False, comment="osm2pgsql osm_id of the source object"),
        sa.Column("name", sa.Text(), nullable=True, comment="Name of the source object, when tagged"),
        sa.Column(
            "legal_basis", sa.Text(), nullable=False, comment="Short reference to the rule that defines the zone"
        ),
        sa.Column(
            "width_m",
            sa.Float(),
            nullable=False,
            comment="Buffer width around the source object in meters; 0 for the object itself",
        ),
        sa.Column(
            "attributes",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            comment="Source attributes the width was derived from",
        ),
        sa.Column(
            "rules_version",
            sa.String(length=64),
            nullable=False,
            comment="Hash of the zone rules file the zone was built with",
        ),
        # The GIST index is created explicitly below, not by the column type.
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(geometry_type="MULTIPOLYGON", srid=3857, spatial_index=False),
            nullable=False,
            comment="Zone geometry in SRID 3857 (Web Mercator)",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_zones")),
        schema="restriction",
    )
    op.create_index("idx_zones_geom", "zones", ["geom"], unique=False, schema="restriction", postgresql_using="gist")
    op.create_index(op.f("ix_restriction_zones_kind"), "zones", ["kind"], unique=False, schema="restriction")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_restriction_zones_kind"), table_name="zones", schema="restriction")
    op.drop_index("idx_zones_geom", table_name="zones", schema="restriction", postgresql_using="gist")
    op.drop_table("zones", schema="restriction")

"""Add topography metrics table.

Revision ID: 674e5b6df11e
Revises: 15c4a02c5334
Create Date: 2026-07-22 14:28:47.854495

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "674e5b6df11e"
down_revision: str | Sequence[str] | None = "15c4a02c5334"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "metrics",
        sa.Column("parcel_id", sa.UUID(), nullable=False, comment="ID of the parcel these metrics belong to"),
        sa.Column("mean_elevation", sa.Float(), nullable=False, comment="Mean elevation in meters"),
        sa.Column("max_elevation", sa.Float(), nullable=False, comment="Maximum elevation in meters"),
        sa.Column("min_elevation", sa.Float(), nullable=False, comment="Minimum elevation in meters"),
        sa.Column("elevation_range", sa.Float(), nullable=False, comment="Elevation range (max - min) in meters"),
        sa.Column("elevation_std", sa.Float(), nullable=False, comment="Standard deviation of elevation in meters"),
        sa.Column("mean_slope", sa.Float(), nullable=False, comment="Mean slope in degrees"),
        sa.Column("max_slope", sa.Float(), nullable=False, comment="Maximum slope in degrees"),
        sa.Column(
            "slope_percentiles",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            comment="Slope values at percentiles 25, 50, 75, 90 as JSON dict",
        ),
        sa.Column(
            "slope_distribution",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            comment="Slope histogram bins (10 bins, 0-90°) as JSON array",
        ),
        sa.Column(
            "aspect",
            sa.String(length=4),
            nullable=False,
            comment="Dominant slope aspect direction (N/NE/E/SE/S/SW/W/NW/FLAT)",
        ),
        sa.Column(
            "south_aspect_percentage",
            sa.Float(),
            nullable=False,
            comment="Percentage of area facing south (SE, S, SW)",
        ),
        sa.Column("area", sa.Float(), nullable=False, comment="Parcel area in square meters"),
        sa.Column("perimeter", sa.Float(), nullable=False, comment="Parcel perimeter in meters"),
        sa.Column(
            "compactness_index",
            sa.Float(),
            nullable=False,
            comment="Compactness index (4πA/P²), dimensionless",
        ),
        sa.Column(
            "elongation_index",
            sa.Float(),
            nullable=False,
            comment="Elongation index (width/length), dimensionless",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parcel_id"],
            ["parcel.parcels.id"],
            name=op.f("fk_metrics_parcel_id_parcels"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_metrics")),
        schema="topography",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("metrics", schema="topography")

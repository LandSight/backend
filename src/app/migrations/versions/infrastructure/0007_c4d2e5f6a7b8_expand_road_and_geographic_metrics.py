"""Expand road and geographic position metrics.

Road accessibility gains distance to the nearest main road and to the nearest
drivable road of any class. Geographic position is split into distances to the
nearest regional center, district center and local settlement, dropping the
previous single major-city distance and city tier.

Revision ID: c4d2e5f6a7b8
Revises: b2f4a1c7d903
Create Date: 2026-09-24 10:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "c4d2e5f6a7b8"
down_revision: str | Sequence[str] | None = "b2f4a1c7d903"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "parcel_road_accessibility_metrics",
        sa.Column(
            "distance_to_main_road",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest main road in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )
    op.add_column(
        "parcel_road_accessibility_metrics",
        sa.Column(
            "distance_to_any_road",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest drivable road in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )

    op.add_column(
        "parcel_geographic_position_metrics",
        sa.Column(
            "distance_to_regional_center",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest regional center in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )
    op.add_column(
        "parcel_geographic_position_metrics",
        sa.Column(
            "distance_to_district_center",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest district center in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )
    op.add_column(
        "parcel_geographic_position_metrics",
        sa.Column(
            "distance_to_settlement",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest local settlement in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )

    op.drop_column("parcel_geographic_position_metrics", "distance_to_major_city", schema="infrastructure")
    op.drop_column("parcel_geographic_position_metrics", "city_tier", schema="infrastructure")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "parcel_geographic_position_metrics",
        sa.Column("city_tier", sa.Text(), nullable=True, comment="Tier of the nearest major city"),
        schema="infrastructure",
    )
    op.add_column(
        "parcel_geographic_position_metrics",
        sa.Column(
            "distance_to_major_city",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest major city in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )

    op.drop_column("parcel_geographic_position_metrics", "distance_to_settlement", schema="infrastructure")
    op.drop_column("parcel_geographic_position_metrics", "distance_to_district_center", schema="infrastructure")
    op.drop_column("parcel_geographic_position_metrics", "distance_to_regional_center", schema="infrastructure")

    op.drop_column("parcel_road_accessibility_metrics", "distance_to_any_road", schema="infrastructure")
    op.drop_column("parcel_road_accessibility_metrics", "distance_to_main_road", schema="infrastructure")

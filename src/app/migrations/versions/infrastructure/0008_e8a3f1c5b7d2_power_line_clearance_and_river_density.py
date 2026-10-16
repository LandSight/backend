"""Add power line clearance and river density metrics.

Utility metrics gain the clearance from the nearest transmission line
protection zone and the distance to the nearest distribution line. Ecology
metrics gain the river density of water bodies.

Revision ID: e8a3f1c5b7d2
Revises: c4d2e5f6a7b8
Create Date: 2026-10-09 16:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "e8a3f1c5b7d2"
down_revision: str | Sequence[str] | None = "c4d2e5f6a7b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "parcel_utility_metrics",
        sa.Column(
            "transmission_line_clearance",
            sa.Float(),
            nullable=True,
            comment="Gap between the parcel and the nearest transmission line protection zone in meters, "
            "0 inside the zone, or NULL if none found",
        ),
        schema="infrastructure",
    )
    op.add_column(
        "parcel_utility_metrics",
        sa.Column(
            "distance_to_distribution_line",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest distribution power line in meters, or NULL if none found",
        ),
        schema="infrastructure",
    )
    op.add_column(
        "parcel_ecology_metrics",
        sa.Column(
            "river_density",
            sa.Float(),
            nullable=True,
            comment="River length per buffer ring area in km/km2 (water bodies only), or NULL",
        ),
        schema="infrastructure",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("parcel_ecology_metrics", "river_density", schema="infrastructure")
    op.drop_column("parcel_utility_metrics", "distance_to_distribution_line", schema="infrastructure")
    op.drop_column("parcel_utility_metrics", "transmission_line_clearance", schema="infrastructure")

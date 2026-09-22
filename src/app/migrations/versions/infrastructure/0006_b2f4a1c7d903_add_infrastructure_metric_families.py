"""Add infrastructure metric family tables.

Consolidates the per-category metrics tables into family tables that share a
metric shape and are disambiguated by a type column: facility (school,
hospital, grocery, bus stop, railway station), ecology (water body, forest,
protected area), utility (power line, gas / water pipeline), road
accessibility and geographic position.

Revision ID: b2f4a1c7d903
Revises: 518e41ca57ed
Create Date: 2026-09-22 10:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "b2f4a1c7d903"
down_revision: str | Sequence[str] | None = "518e41ca57ed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _timestamps() -> list[sa.Column]:
    return [
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
    ]


def _parcel_id_column() -> sa.Column:
    return sa.Column(
        "parcel_id",
        sa.UUID(),
        nullable=False,
        comment="ID of the parcel these metrics belong to",
    )


def _buffer_column() -> sa.Column:
    return sa.Column(
        "buffer",
        sa.Integer(),
        nullable=False,
        comment="Buffer radius in meters around the parcel boundary",
    )


def _foreign_key(table: str) -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(
        ["parcel_id"],
        ["parcel.parcels.id"],
        name=op.f(f"fk_{table}_parcel_id_parcels"),
        ondelete="CASCADE",
    )


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "parcel_facility_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column(
            "facility_type",
            sa.Text(),
            nullable=False,
            comment="Facility category (school, hospital, grocery, bus_stop, railway_station)",
        ),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of facility objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest facility in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_facility_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_facility_metrics")),
        schema="infrastructure",
    )

    op.create_table(
        "parcel_ecology_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column(
            "object_type",
            sa.Text(),
            nullable=False,
            comment="Ecology category (water_body, forest, protected_area)",
        ),
        sa.Column(
            "coverage_ratio",
            sa.Float(),
            nullable=False,
            comment="Fraction of the buffer zone covered by the objects in [0, 1]",
        ),
        sa.Column(
            "count",
            sa.Integer(),
            nullable=False,
            comment="Number of distinct (connected) objects within the buffer",
        ),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest object in meters, or NULL if none found",
        ),
        sa.Column(
            "distance_to_large_object",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest large object in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_ecology_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_ecology_metrics")),
        schema="infrastructure",
    )

    op.create_table(
        "parcel_utility_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column(
            "utility_type",
            sa.Text(),
            nullable=False,
            comment="Utility category (power_line, gas_pipeline, water_pipeline)",
        ),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest utility network in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_utility_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_utility_metrics")),
        schema="infrastructure",
    )

    op.create_table(
        "parcel_road_accessibility_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column(
            "distance_to_paved_road",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest paved road in meters, or NULL if none found",
        ),
        sa.Column(
            "road_density_1km",
            sa.Float(),
            nullable=False,
            comment="Road network density within the buffer in km/km2",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_road_accessibility_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_road_accessibility_metrics")),
        schema="infrastructure",
    )

    op.create_table(
        "parcel_geographic_position_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column(
            "distance_to_major_city",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest major city in meters, or NULL if none found",
        ),
        sa.Column(
            "city_tier",
            sa.Text(),
            nullable=False,
            comment="Tier of the nearest major city (regional_center, district_center, local_town, unknown)",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_geographic_position_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_geographic_position_metrics")),
        schema="infrastructure",
    )

    op.drop_table("parcel_water_body_metrics", schema="infrastructure")
    op.drop_table("parcel_shop_metrics", schema="infrastructure")
    op.drop_table("parcel_transit_stop_metrics", schema="infrastructure")
    op.drop_table("parcel_hospital_metrics", schema="infrastructure")
    op.drop_table("parcel_school_metrics", schema="infrastructure")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "parcel_school_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of school objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest school in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_school_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_school_metrics")),
        schema="infrastructure",
    )
    op.create_table(
        "parcel_hospital_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of hospital objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest hospital in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_hospital_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_hospital_metrics")),
        schema="infrastructure",
    )
    op.create_table(
        "parcel_transit_stop_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of transit stop objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest transit stop in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_transit_stop_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_transit_stop_metrics")),
        schema="infrastructure",
    )
    op.create_table(
        "parcel_shop_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of shop objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest shop in meters, or NULL if none found",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_shop_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_shop_metrics")),
        schema="infrastructure",
    )
    op.create_table(
        "parcel_water_body_metrics",
        _parcel_id_column(),
        _buffer_column(),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of water body objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest water body in meters, or NULL if none found",
        ),
        sa.Column(
            "coverage_ratio",
            sa.Float(),
            nullable=False,
            comment="Fraction of the buffer zone covered by water bodies in [0, 1]",
        ),
        *_timestamps(),
        sa.Column("id", sa.UUID(), nullable=False),
        _foreign_key("parcel_water_body_metrics"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_water_body_metrics")),
        schema="infrastructure",
    )

    op.drop_table("parcel_geographic_position_metrics", schema="infrastructure")
    op.drop_table("parcel_road_accessibility_metrics", schema="infrastructure")
    op.drop_table("parcel_utility_metrics", schema="infrastructure")
    op.drop_table("parcel_ecology_metrics", schema="infrastructure")
    op.drop_table("parcel_facility_metrics", schema="infrastructure")

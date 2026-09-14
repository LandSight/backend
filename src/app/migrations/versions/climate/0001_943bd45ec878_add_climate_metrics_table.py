"""Add climate metrics table.

Revision ID: 943bd45ec878
Revises:
Create Date: 2026-09-06 13:38:43.117922

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "943bd45ec878"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "metrics",
        sa.Column("parcel_id", sa.UUID(), nullable=False, comment="ID of the parcel these metrics belong to"),
        sa.Column(
            "mean_annual_temperature", sa.Float(), nullable=False, comment="Mean annual temperature (BIO1) in °C"
        ),
        sa.Column("annual_precipitation", sa.Float(), nullable=False, comment="Annual precipitation (BIO12) in mm"),
        sa.Column(
            "temperature_seasonality", sa.Float(), nullable=False, comment="Temperature seasonality (BIO4) in °C"
        ),
        sa.Column(
            "precipitation_seasonality",
            sa.Float(),
            nullable=False,
            comment="Precipitation seasonality (BIO15), coefficient of variation in %",
        ),
        sa.Column(
            "max_temperature_warmest_month",
            sa.Float(),
            nullable=False,
            comment="Max temperature of the warmest month (BIO5) in °C",
        ),
        sa.Column(
            "min_temperature_coldest_month",
            sa.Float(),
            nullable=False,
            comment="Min temperature of the coldest month (BIO6) in °C",
        ),
        sa.Column(
            "precipitation_wettest_month",
            sa.Float(),
            nullable=False,
            comment="Precipitation of the wettest month (BIO13) in mm",
        ),
        sa.Column(
            "precipitation_driest_month",
            sa.Float(),
            nullable=False,
            comment="Precipitation of the driest month (BIO14) in mm",
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parcel_id"], ["parcel.parcels.id"], name=op.f("fk_metrics_parcel_id_parcels"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_metrics")),
        schema="climate",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("metrics", schema="climate")

"""Add infrastructure school metrics table.

Revision ID: 518e41ca57ed
Revises: 5686f4012cee
Create Date: 2026-09-05 16:38:55.552029

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "518e41ca57ed"
down_revision: str | Sequence[str] | None = "5686f4012cee"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "parcel_school_metrics",
        sa.Column(
            "parcel_id",
            sa.UUID(),
            nullable=False,
            comment="ID of the parcel these metrics belong to",
        ),
        sa.Column("buffer", sa.Integer(), nullable=False, comment="Buffer radius in meters around the parcel boundary"),
        sa.Column("count", sa.Integer(), nullable=False, comment="Number of school objects within the buffer"),
        sa.Column(
            "min_distance_to",
            sa.Float(),
            nullable=True,
            comment="Distance to the nearest school in meters, or NULL if none found",
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
            name=op.f("fk_parcel_school_metrics_parcel_id_parcels"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_school_metrics")),
        schema="infrastructure",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("parcel_school_metrics", schema="infrastructure")

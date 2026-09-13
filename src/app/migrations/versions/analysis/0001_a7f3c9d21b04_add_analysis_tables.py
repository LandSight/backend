"""Add analysis tables.

Revision ID: a7f3c9d21b04
Revises:
Create Date: 2026-09-12 09:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "a7f3c9d21b04"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "analyses",
        sa.Column("parcel_id", sa.UUID(), nullable=False, comment="ID of the parcel being analysed"),
        sa.Column("name", sa.String(length=64), nullable=False, comment="Human-readable analysis name"),
        sa.Column(
            "status",
            sa.String(length=16),
            nullable=False,
            comment="Lifecycle status (pending/running/completed/failed)",
        ),
        sa.Column("score", sa.Float(), nullable=True, comment="Final score in [0, 10]; NULL until completed"),
        sa.Column(
            "status_reason",
            sa.String(length=512),
            nullable=True,
            comment="Human-readable status explanation",
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
            name=op.f("fk_analyses_parcel_id_parcels"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analyses")),
        schema="analysis",
    )
    op.create_table(
        "analysis_metrics",
        sa.Column("analysis_id", sa.UUID(), nullable=False, comment="ID of the owning analysis"),
        sa.Column(
            "metric_type",
            sa.String(length=32),
            nullable=False,
            comment="Metric module (topography/climate/infrastructure)",
        ),
        sa.Column(
            "category",
            sa.String(length=32),
            nullable=True,
            comment="Infrastructure category; NULL for single-metric modules",
        ),
        sa.Column("metric_id", sa.UUID(), nullable=False, comment="ID of the referenced metrics snapshot"),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["analysis.analyses.id"],
            name=op.f("fk_analysis_metrics_analysis_id_analyses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_metrics")),
        schema="analysis",
    )
    op.create_index(
        op.f("ix_analysis_metrics_analysis_id"),
        "analysis_metrics",
        ["analysis_id"],
        unique=False,
        schema="analysis",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_analysis_metrics_analysis_id"), table_name="analysis_metrics", schema="analysis")
    op.drop_table("analysis_metrics", schema="analysis")
    op.drop_table("analyses", schema="analysis")

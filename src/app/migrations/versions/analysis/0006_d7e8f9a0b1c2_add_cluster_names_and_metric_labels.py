"""Add cluster names and metric labels.

Revision ID: d7e8f9a0b1c2
Revises: c3a7e91b04f2
Create Date: 2026-09-30 08:15:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "d7e8f9a0b1c2"
down_revision: str | Sequence[str] | None = "c3a7e91b04f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "analysis_cluster_scores",
        sa.Column(
            "name",
            sa.String(length=128),
            server_default="",
            nullable=False,
            comment="Human-readable group name; empty when not configured",
        ),
        schema="analysis",
    )
    op.add_column(
        "analysis_metric_contributions",
        sa.Column(
            "label",
            sa.String(length=128),
            server_default="",
            nullable=False,
            comment="Human-readable metric name; empty when not available",
        ),
        schema="analysis",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("analysis_metric_contributions", "label", schema="analysis")
    op.drop_column("analysis_cluster_scores", "name", schema="analysis")

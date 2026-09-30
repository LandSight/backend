"""Add analysis type and evaluation metadata columns.

Revision ID: d4f7a1c93e20
Revises: b1d4e7f90a32
Create Date: 2026-09-25 08:30:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "d4f7a1c93e20"
down_revision: str | Sequence[str] | None = "b1d4e7f90a32"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "analyses",
        sa.Column(
            "analysis_type",
            sa.String(length=32),
            nullable=False,
            server_default="izhs",
            comment="Evaluation profile (e.g. izhs)",
        ),
        schema="analysis",
    )
    op.alter_column("analyses", "analysis_type", server_default=None, schema="analysis")
    op.add_column(
        "analyses",
        sa.Column(
            "model_version",
            sa.String(length=32),
            nullable=True,
            comment="Version of the scoring model; NULL until completed",
        ),
        schema="analysis",
    )
    op.add_column(
        "analyses",
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
            comment="When the analysis completed (UTC); NULL until completed",
        ),
        schema="analysis",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("analyses", "completed_at", schema="analysis")
    op.drop_column("analyses", "model_version", schema="analysis")
    op.drop_column("analyses", "analysis_type", schema="analysis")

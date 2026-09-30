"""Add analysis engine columns.

Revision ID: c3a7e91b04f2
Revises: f1c8b3a52d90
Create Date: 2026-09-28 08:10:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "c3a7e91b04f2"
down_revision: str | Sequence[str] | None = "f1c8b3a52d90"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "analyses",
        sa.Column(
            "engine",
            sa.String(length=32),
            nullable=False,
            server_default="baseline",
            comment="Scoring engine (e.g. baseline)",
        ),
        schema="analysis",
    )
    op.alter_column("analyses", "engine", server_default=None, schema="analysis")

    op.add_column(
        "analysis_evaluations",
        sa.Column(
            "engine",
            sa.String(length=32),
            nullable=False,
            server_default="baseline",
            comment="Scoring engine (e.g. baseline)",
        ),
        schema="analysis",
    )
    op.alter_column("analysis_evaluations", "engine", server_default=None, schema="analysis")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("analysis_evaluations", "engine", schema="analysis")
    op.drop_column("analyses", "engine", schema="analysis")

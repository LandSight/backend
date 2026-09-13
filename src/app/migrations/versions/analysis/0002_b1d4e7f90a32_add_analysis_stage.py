"""Add analysis stage column.

Revision ID: b1d4e7f90a32
Revises: a7f3c9d21b04
Create Date: 2026-09-13 08:40:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "b1d4e7f90a32"
down_revision: str | Sequence[str] | None = "a7f3c9d21b04"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "analyses",
        sa.Column(
            "stage",
            sa.String(length=16),
            nullable=False,
            server_default="metrics",
            comment="Pipeline stage (metrics/scoring)",
        ),
        schema="analysis",
    )
    op.alter_column("analyses", "stage", server_default=None, schema="analysis")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("analyses", "stage", schema="analysis")

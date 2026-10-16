"""Add analysis restriction checks.

Restrictions are not metrics: the reference to the restriction check an
analysis was scored with moves from ``analysis_metrics`` to its own table.

Revision ID: ede5374bb2bc
Revises: fcaa4832215f
Create Date: 2026-10-16 11:00:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "ede5374bb2bc"
down_revision: str | Sequence[str] | None = "fcaa4832215f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "analysis_restriction_checks",
        sa.Column("analysis_id", sa.UUID(), nullable=False, comment="ID of the owning analysis"),
        sa.Column(
            "check_id",
            sa.UUID(),
            nullable=False,
            comment="ID of the restriction check snapshot (weak reference)",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["analysis_id"],
            ["analysis.analyses.id"],
            name=op.f("fk_analysis_restriction_checks_analysis_id_analyses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_restriction_checks")),
        sa.UniqueConstraint("analysis_id", name=op.f("uq_analysis_restriction_checks_analysis_id")),
        schema="analysis",
    )
    # Move the references collected while restrictions were a metric module.
    op.execute(
        """
        INSERT INTO analysis.analysis_restriction_checks (id, analysis_id, check_id)
        SELECT DISTINCT ON (analysis_id) gen_random_uuid(), analysis_id, metric_id
        FROM analysis.analysis_metrics
        WHERE metric_type = 'restriction'
        """
    )
    op.execute("DELETE FROM analysis.analysis_metrics WHERE metric_type = 'restriction'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        INSERT INTO analysis.analysis_metrics (id, analysis_id, metric_type, metric_id)
        SELECT gen_random_uuid(), analysis_id, 'restriction', check_id
        FROM analysis.analysis_restriction_checks
        """
    )
    op.drop_table("analysis_restriction_checks", schema="analysis")

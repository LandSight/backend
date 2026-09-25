"""Add analysis evaluation score tables.

Revision ID: f1c8b3a52d90
Revises: d4f7a1c93e20
Create Date: 2026-09-25 08:40:00.000000

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "f1c8b3a52d90"
down_revision: str | Sequence[str] | None = "d4f7a1c93e20"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "analysis_evaluations",
        sa.Column("analysis_id", sa.UUID(), nullable=False, comment="ID of the owning analysis"),
        sa.Column("analysis_type", sa.String(length=32), nullable=False, comment="Evaluation profile (e.g. izhs)"),
        sa.Column(
            "model_version",
            sa.String(length=32),
            nullable=False,
            comment="Version of the hierarchy and normalization configuration used",
        ),
        sa.Column("total_score", sa.Float(), nullable=False, comment="Final score on the 0-10 scale"),
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
            ["analysis_id"],
            ["analysis.analyses.id"],
            name=op.f("fk_analysis_evaluations_analysis_id_analyses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_evaluations")),
        schema="analysis",
    )
    op.create_index(
        op.f("ix_analysis_evaluations_analysis_id"),
        "analysis_evaluations",
        ["analysis_id"],
        unique=False,
        schema="analysis",
    )

    op.create_table(
        "analysis_cluster_scores",
        sa.Column("evaluation_id", sa.UUID(), nullable=False, comment="ID of the owning evaluation"),
        sa.Column(
            "parent_id", sa.UUID(), nullable=True, comment="ID of the parent group; NULL for a top-level cluster"
        ),
        sa.Column("key", sa.String(length=64), nullable=False, comment="Group key (e.g. relief or slope)"),
        sa.Column("depth", sa.Integer(), nullable=False, comment="Nesting depth; 0 for a top-level cluster"),
        sa.Column("score", sa.Float(), nullable=False, comment="Aggregated group score in [0, 1]"),
        sa.Column("weight", sa.Float(), nullable=False, comment="Configured group weight"),
        sa.Column("contribution", sa.Float(), nullable=False, comment="score * weight"),
        sa.Column("position", sa.Integer(), nullable=False, comment="Display order within the parent"),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            ["analysis.analysis_evaluations.id"],
            name=op.f("fk_analysis_cluster_scores_evaluation_id_analysis_evaluations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["analysis.analysis_cluster_scores.id"],
            name=op.f("fk_analysis_cluster_scores_parent_id_analysis_cluster_scores"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_cluster_scores")),
        schema="analysis",
    )
    op.create_index(
        op.f("ix_analysis_cluster_scores_evaluation_id"),
        "analysis_cluster_scores",
        ["evaluation_id"],
        unique=False,
        schema="analysis",
    )
    op.create_index(
        op.f("ix_analysis_cluster_scores_parent_id"),
        "analysis_cluster_scores",
        ["parent_id"],
        unique=False,
        schema="analysis",
    )

    op.create_table(
        "analysis_metric_contributions",
        sa.Column("evaluation_id", sa.UUID(), nullable=False, comment="ID of the owning evaluation"),
        sa.Column("cluster_score_id", sa.UUID(), nullable=False, comment="ID of the group this metric belongs to"),
        sa.Column("metric_key", sa.String(length=64), nullable=False, comment="Metric key"),
        sa.Column("position", sa.Integer(), nullable=False, comment="Display order within its group"),
        sa.Column("raw_value", sa.Float(), nullable=True, comment="Raw metric reading; NULL when unavailable"),
        sa.Column(
            "normalized_value",
            sa.Float(),
            nullable=True,
            comment="Normalized value in [0, 1]; NULL when unavailable",
        ),
        sa.Column("weight", sa.Float(), nullable=False, comment="Configured weight among siblings"),
        sa.Column("contribution", sa.Float(), nullable=True, comment="normalized_value * weight"),
        sa.Column("unit", sa.String(length=32), nullable=False, comment="Unit of the raw value"),
        sa.Column(
            "membership_function",
            sa.String(length=32),
            nullable=True,
            comment="Name of the applied membership function",
        ),
        sa.Column(
            "membership_params",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment="Parameters of the applied membership function",
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["evaluation_id"],
            ["analysis.analysis_evaluations.id"],
            name=op.f("fk_analysis_metric_contributions_evaluation_id_analysis_evaluations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["cluster_score_id"],
            ["analysis.analysis_cluster_scores.id"],
            name=op.f("fk_analysis_metric_contributions_cluster_score_id_analysis_cluster_scores"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analysis_metric_contributions")),
        schema="analysis",
    )
    op.create_index(
        op.f("ix_analysis_metric_contributions_evaluation_id"),
        "analysis_metric_contributions",
        ["evaluation_id"],
        unique=False,
        schema="analysis",
    )
    op.create_index(
        op.f("ix_analysis_metric_contributions_cluster_score_id"),
        "analysis_metric_contributions",
        ["cluster_score_id"],
        unique=False,
        schema="analysis",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_analysis_metric_contributions_cluster_score_id"),
        table_name="analysis_metric_contributions",
        schema="analysis",
    )
    op.drop_index(
        op.f("ix_analysis_metric_contributions_evaluation_id"),
        table_name="analysis_metric_contributions",
        schema="analysis",
    )
    op.drop_table("analysis_metric_contributions", schema="analysis")
    op.drop_index(
        op.f("ix_analysis_cluster_scores_parent_id"),
        table_name="analysis_cluster_scores",
        schema="analysis",
    )
    op.drop_index(
        op.f("ix_analysis_cluster_scores_evaluation_id"),
        table_name="analysis_cluster_scores",
        schema="analysis",
    )
    op.drop_table("analysis_cluster_scores", schema="analysis")
    op.drop_index(
        op.f("ix_analysis_evaluations_analysis_id"),
        table_name="analysis_evaluations",
        schema="analysis",
    )
    op.drop_table("analysis_evaluations", schema="analysis")

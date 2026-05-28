"""add app_logs table

Revision ID: 0002_app_logs
Revises: 0001_init
Create Date: 2026-05-28
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = "0002_app_logs"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("level", sa.String(length=20), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=False),
        sa.Column("method", sa.String(length=10), nullable=True),
        sa.Column("path", sa.String(length=255), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("request_id", sa.String(length=64), nullable=True),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.create_index("ix_app_logs_level", "app_logs", ["level"], unique=False)
    op.create_index("ix_app_logs_request_id", "app_logs", ["request_id"], unique=False)
    op.create_index("ix_app_logs_owner_id", "app_logs", ["owner_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_app_logs_owner_id", table_name="app_logs")
    op.drop_index("ix_app_logs_request_id", table_name="app_logs")
    op.drop_index("ix_app_logs_level", table_name="app_logs")
    op.drop_table("app_logs")


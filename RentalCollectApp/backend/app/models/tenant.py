from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Tenant(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tenants"

    unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("units.id"), index=True, nullable=False)
    tenant_name: Mapped[str] = mapped_column(String(120), nullable=False)
    mobile: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    deposit: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

    unit: Mapped["Unit"] = relationship(back_populates="tenants")
    payments: Mapped[List["Payment"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")


from app.models.payment import Payment  # noqa: E402
from app.models.unit import Unit  # noqa: E402


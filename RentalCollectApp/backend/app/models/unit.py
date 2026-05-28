from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Unit(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "units"

    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("properties.id"), index=True, nullable=False
    )

    unit_name: Mapped[str] = mapped_column(String(80), nullable=False)
    rent_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    property: Mapped["Property"] = relationship(back_populates="units")
    tenants: Mapped[List["Tenant"]] = relationship(back_populates="unit", cascade="all, delete-orphan")


from app.models.property import Property  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402


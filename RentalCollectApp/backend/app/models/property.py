from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Property(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "properties"

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("owners.id"), index=True, nullable=False)

    property_name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    owner: Mapped["Owner"] = relationship(back_populates="properties")
    units: Mapped[List["Unit"]] = relationship(back_populates="property", cascade="all, delete-orphan")


from app.models.owner import Owner  # noqa: E402
from app.models.unit import Unit  # noqa: E402


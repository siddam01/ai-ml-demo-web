from __future__ import annotations

import uuid
from decimal import Decimal

from pydantic import Field

from app.schemas.common import APIModel, MobileValidated, TimestampedModel, UUIDModel


class TenantCreate(MobileValidated):
    unit_id: uuid.UUID
    tenant_name: str = Field(..., min_length=1, max_length=120)
    deposit: Decimal | None = Field(default=None, ge=0)


class TenantUpdate(APIModel):
    tenant_name: str | None = Field(default=None, min_length=1, max_length=120)
    mobile: str | None = None
    deposit: Decimal | None = Field(default=None, ge=0)


class TenantPublic(UUIDModel, TimestampedModel, MobileValidated):
    unit_id: uuid.UUID
    tenant_name: str
    deposit: Decimal | None


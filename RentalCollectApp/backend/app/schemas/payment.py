from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from pydantic import Field

from app.schemas.common import APIModel, TimestampedModel, UUIDModel


class PaymentCreate(APIModel):
    tenant_id: uuid.UUID
    amount: Decimal = Field(..., gt=0)
    payment_date: date
    status: str = Field(default="paid", max_length=20)
    note: str | None = Field(default=None, max_length=255)


class PaymentPublic(UUIDModel, TimestampedModel):
    tenant_id: uuid.UUID
    amount: Decimal
    payment_date: date
    status: str
    note: str | None


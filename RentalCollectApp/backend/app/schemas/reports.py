from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from pydantic import Field

from app.schemas.common import APIModel


class CollectionSummary(APIModel):
    from_date: date
    to_date: date
    total_received: Decimal = Field(..., ge=0)
    total_payments: int = Field(..., ge=0)


class TenantDue(APIModel):
    tenant_id: uuid.UUID
    tenant_name: str
    unit_id: uuid.UUID
    unit_name: str
    property_id: uuid.UUID
    property_name: str
    monthly_rent: Decimal = Field(..., ge=0)
    last_payment_date: date | None
    due_amount_estimate: Decimal = Field(..., ge=0)


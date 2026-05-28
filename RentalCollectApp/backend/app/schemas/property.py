from __future__ import annotations

import uuid
from decimal import Decimal

from pydantic import Field

from app.schemas.common import APIModel, TimestampedModel, UUIDModel


class PropertyCreate(APIModel):
    property_name: str = Field(..., min_length=1, max_length=200)
    address: str | None = None


class PropertyUpdate(APIModel):
    property_name: str | None = Field(default=None, min_length=1, max_length=200)
    address: str | None = None


class PropertyPublic(UUIDModel, TimestampedModel):
    owner_id: uuid.UUID
    property_name: str
    address: str | None


class UnitCreate(APIModel):
    unit_name: str = Field(..., min_length=1, max_length=80)
    rent_amount: Decimal = Field(..., gt=0)


class UnitPublic(UUIDModel, TimestampedModel):
    property_id: uuid.UUID
    unit_name: str
    rent_amount: Decimal


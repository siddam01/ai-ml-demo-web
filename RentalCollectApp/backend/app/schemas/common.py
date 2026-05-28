from __future__ import annotations

import re
import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


MOBILE_RE = re.compile(r"^\+?[0-9]{10,15}$")


class APIModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UUIDModel(APIModel):
    id: uuid.UUID


class TimestampedModel(APIModel):
    created_at: datetime
    updated_at: datetime


class MobileValidated(APIModel):
    mobile: str = Field(..., examples=["+919999999999", "9999999999"])

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        v = v.strip()
        if not MOBILE_RE.match(v):
            raise ValueError("Mobile must be 10-15 digits, optionally starting with '+'")
        return v


class MoneyValidated(APIModel):
    amount: Decimal = Field(..., gt=0)


class DateValidated(APIModel):
    payment_date: date


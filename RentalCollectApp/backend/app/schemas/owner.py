from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from app.schemas.common import APIModel, MobileValidated, TimestampedModel, UUIDModel


class OwnerCreate(MobileValidated):
    name: str = Field(..., min_length=1, max_length=120)
    password: str = Field(..., min_length=8, max_length=128)


class OwnerPublic(UUIDModel, TimestampedModel, MobileValidated):
    name: str


class TokenPair(APIModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(APIModel):
    refresh_token: str


class LoginRequest(MobileValidated):
    password: str


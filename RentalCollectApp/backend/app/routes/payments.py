from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_owner, get_session
from app.models.owner import Owner
from app.schemas.payment import PaymentCreate, PaymentPublic
from app.services.payments import PaymentService


router = APIRouter()


@router.get("", response_model=list[PaymentPublic])
async def list_payments_for_tenant(
    tenant_id: uuid.UUID,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PaymentService(session).list_for_tenant(owner_id=owner.id, tenant_id=tenant_id)


@router.post("", response_model=PaymentPublic, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreate,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PaymentService(session).create(owner_id=owner.id, payload=payload)


from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_owner, get_session
from app.models.owner import Owner
from app.schemas.tenant import TenantCreate, TenantPublic, TenantUpdate
from app.services.tenants import TenantService


router = APIRouter()


@router.get("", response_model=list[TenantPublic])
async def list_tenants_for_unit(
    unit_id: uuid.UUID,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await TenantService(session).list_for_unit(owner_id=owner.id, unit_id=unit_id)


@router.post("", response_model=TenantPublic, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    payload: TenantCreate,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await TenantService(session).create(owner_id=owner.id, payload=payload)


@router.patch("/{tenant_id}", response_model=TenantPublic)
async def update_tenant(
    tenant_id: uuid.UUID,
    payload: TenantUpdate,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await TenantService(session).update(owner_id=owner.id, tenant_id=tenant_id, payload=payload)


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tenant(
    tenant_id: uuid.UUID,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    await TenantService(session).delete(owner_id=owner.id, tenant_id=tenant_id)
    return None

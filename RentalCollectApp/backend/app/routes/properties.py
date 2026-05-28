from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_owner, get_session
from app.models.owner import Owner
from app.schemas.property import PropertyCreate, PropertyPublic, PropertyUpdate, UnitCreate, UnitPublic
from app.services.properties import PropertyService


router = APIRouter()


@router.get("", response_model=list[PropertyPublic])
async def list_properties(
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PropertyService(session).list_properties(owner_id=owner.id)


@router.post("", response_model=PropertyPublic, status_code=status.HTTP_201_CREATED)
async def create_property(
    payload: PropertyCreate,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PropertyService(session).create_property(owner_id=owner.id, payload=payload)


@router.patch("/{property_id}", response_model=PropertyPublic)
async def update_property(
    property_id: uuid.UUID,
    payload: PropertyUpdate,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PropertyService(session).update_property(owner_id=owner.id, property_id=property_id, payload=payload)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: uuid.UUID,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    await PropertyService(session).delete_property(owner_id=owner.id, property_id=property_id)
    return None


@router.get("/{property_id}/units", response_model=list[UnitPublic])
async def list_units(
    property_id: uuid.UUID,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PropertyService(session).list_units(owner_id=owner.id, property_id=property_id)


@router.post("/{property_id}/units", response_model=UnitPublic, status_code=status.HTTP_201_CREATED)
async def create_unit(
    property_id: uuid.UUID,
    payload: UnitCreate,
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
):
    return await PropertyService(session).create_unit(owner_id=owner.id, property_id=property_id, payload=payload)


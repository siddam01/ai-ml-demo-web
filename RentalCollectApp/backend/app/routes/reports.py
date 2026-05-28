from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_owner, get_session
from app.models.owner import Owner
from app.schemas.reports import CollectionSummary, TenantDue
from app.services.reports import ReportService


router = APIRouter()


@router.get("/collection-summary", response_model=CollectionSummary)
async def collection_summary(
    from_date: date = Query(...),
    to_date: date = Query(...),
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
) -> CollectionSummary:
    return await ReportService(session).collection_summary(owner_id=owner.id, from_date=from_date, to_date=to_date)


@router.get("/pending-dues", response_model=list[TenantDue])
async def pending_dues(
    as_of: date = Query(...),
    owner: Owner = Depends(get_current_owner),
    session: AsyncSession = Depends(get_session),
) -> list[TenantDue]:
    return await ReportService(session).pending_dues(owner_id=owner.id, as_of=as_of)


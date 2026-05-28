from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session, require_refresh_token
from app.schemas.owner import OwnerCreate, TokenPair, TokenRefreshRequest
from app.services.auth import AuthService


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: OwnerCreate, session: AsyncSession = Depends(get_session)) -> dict:
    owner_id = await AuthService(session).register_owner(payload)
    return {"id": str(owner_id)}


@router.post("/login", response_model=TokenPair)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> TokenPair:
    # OAuth2PasswordRequestForm uses "username" field; we treat it as mobile.
    return await AuthService(session).login(mobile=form.username, password=form.password)


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: TokenRefreshRequest, session: AsyncSession = Depends(get_session)) -> TokenPair:
    owner_id = await require_refresh_token(payload.refresh_token)
    return await AuthService(session).refresh(owner_id=owner_id)


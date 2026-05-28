from __future__ import annotations

import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db_session
from app.repositories.owners import OwnerRepository
from app.utils.exceptions import UnauthorizedError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_session() -> AsyncSession:
    async for session in get_db_session():
        return session
    raise RuntimeError("DB session not available")


async def get_current_owner(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid access token")
    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedError("Invalid token subject")

    try:
        owner_id = uuid.UUID(str(sub))
    except ValueError as e:
        raise UnauthorizedError("Invalid token subject") from e

    owner = await OwnerRepository(session).get_by_id(owner_id)
    if not owner:
        raise UnauthorizedError("Owner not found")
    return owner


async def require_refresh_token(token: str) -> uuid.UUID:
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise UnauthorizedError("Invalid refresh token")
    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedError("Invalid token subject")
    try:
        return uuid.UUID(str(sub))
    except ValueError as e:
        raise UnauthorizedError("Invalid token subject") from e


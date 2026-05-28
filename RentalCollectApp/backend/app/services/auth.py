from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.repositories.owners import OwnerRepository
from app.schemas.owner import OwnerCreate, TokenPair
from app.utils.exceptions import ConflictError, UnauthorizedError


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.owners = OwnerRepository(session)

    async def register_owner(self, payload: OwnerCreate) -> uuid.UUID:
        existing = await self.owners.get_by_mobile(payload.mobile)
        if existing:
            raise ConflictError("Mobile already registered")

        owner = await self.owners.create(
            name=payload.name,
            mobile=payload.mobile,
            password_hash=hash_password(payload.password),
        )
        await self.session.commit()
        return owner.id

    async def login(self, *, mobile: str, password: str) -> TokenPair:
        owner = await self.owners.get_by_mobile(mobile)
        if not owner or not verify_password(password, owner.password_hash):
            raise UnauthorizedError("Invalid credentials")

        access = create_access_token(str(owner.id))
        refresh = create_refresh_token(str(owner.id))
        return TokenPair(access_token=access, refresh_token=refresh)

    async def refresh(self, *, owner_id: uuid.UUID) -> TokenPair:
        access = create_access_token(str(owner_id))
        refresh = create_refresh_token(str(owner_id))
        return TokenPair(access_token=access, refresh_token=refresh)


from __future__ import annotations

import uuid

from sqlalchemy import select

from app.models.owner import Owner
from app.repositories.base import BaseRepository


class OwnerRepository(BaseRepository):
    async def get_by_id(self, owner_id: uuid.UUID) -> Owner | None:
        stmt = select(Owner).where(Owner.id == owner_id, Owner.is_deleted.is_(False))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_mobile(self, mobile: str) -> Owner | None:
        stmt = select(Owner).where(Owner.mobile == mobile, Owner.is_deleted.is_(False))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, *, name: str, mobile: str, password_hash: str) -> Owner:
        owner = Owner(name=name, mobile=mobile, password_hash=password_hash)
        self.session.add(owner)
        await self.session.flush()
        return owner


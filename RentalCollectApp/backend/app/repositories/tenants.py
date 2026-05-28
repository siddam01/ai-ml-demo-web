from __future__ import annotations

import uuid

from sqlalchemy import select

from app.models.tenant import Tenant
from app.repositories.base import BaseRepository


class TenantRepository(BaseRepository):
    async def get(self, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = select(Tenant).where(Tenant.id == tenant_id, Tenant.is_deleted.is_(False))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_for_unit(self, unit_id: uuid.UUID) -> list[Tenant]:
        stmt = select(Tenant).where(Tenant.unit_id == unit_id, Tenant.is_deleted.is_(False)).order_by(Tenant.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create(self, *, unit_id: uuid.UUID, tenant_name: str, mobile: str, deposit) -> Tenant:
        tenant = Tenant(unit_id=unit_id, tenant_name=tenant_name, mobile=mobile, deposit=deposit)
        self.session.add(tenant)
        await self.session.flush()
        return tenant

    async def update(self, tenant: Tenant, *, tenant_name: str | None, mobile: str | None, deposit) -> Tenant:
        if tenant_name is not None:
            tenant.tenant_name = tenant_name
        if mobile is not None:
            tenant.mobile = mobile
        if deposit is not None:
            tenant.deposit = deposit
        await self.session.flush()
        return tenant

    async def soft_delete(self, tenant: Tenant) -> None:
        tenant.is_deleted = True
        await self.session.flush()


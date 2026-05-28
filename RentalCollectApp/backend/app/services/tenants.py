from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property
from app.models.unit import Unit
from app.repositories.tenants import TenantRepository
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.utils.exceptions import NotFoundError


class TenantService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.tenants = TenantRepository(session)

    async def _unit_for_owner(self, *, owner_id: uuid.UUID, unit_id: uuid.UUID) -> Unit | None:
        stmt = (
            select(Unit)
            .join(Property, Property.id == Unit.property_id)
            .where(
                Unit.id == unit_id,
                Unit.is_deleted.is_(False),
                Property.owner_id == owner_id,
                Property.is_deleted.is_(False),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_for_unit(self, *, owner_id: uuid.UUID, unit_id: uuid.UUID):
        unit = await self._unit_for_owner(owner_id=owner_id, unit_id=unit_id)
        if not unit:
            raise NotFoundError("Unit not found")
        return await self.tenants.list_for_unit(unit_id)

    async def create(self, *, owner_id: uuid.UUID, payload: TenantCreate):
        unit = await self._unit_for_owner(owner_id=owner_id, unit_id=payload.unit_id)
        if not unit:
            raise NotFoundError("Unit not found")
        tenant = await self.tenants.create(
            unit_id=payload.unit_id,
            tenant_name=payload.tenant_name,
            mobile=payload.mobile,
            deposit=payload.deposit,
        )
        await self.session.commit()
        return tenant

    async def update(self, *, owner_id: uuid.UUID, tenant_id: uuid.UUID, payload: TenantUpdate):
        tenant = await self.tenants.get(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant not found")
        unit = await self._unit_for_owner(owner_id=owner_id, unit_id=tenant.unit_id)
        if not unit:
            raise NotFoundError("Tenant not found")
        await self.tenants.update(tenant, tenant_name=payload.tenant_name, mobile=payload.mobile, deposit=payload.deposit)
        await self.session.commit()
        return tenant

    async def delete(self, *, owner_id: uuid.UUID, tenant_id: uuid.UUID):
        tenant = await self.tenants.get(tenant_id)
        if not tenant:
            raise NotFoundError("Tenant not found")
        unit = await self._unit_for_owner(owner_id=owner_id, unit_id=tenant.unit_id)
        if not unit:
            raise NotFoundError("Tenant not found")
        await self.tenants.soft_delete(tenant)
        await self.session.commit()


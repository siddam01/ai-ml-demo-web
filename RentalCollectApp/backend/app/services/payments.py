from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property
from app.models.tenant import Tenant
from app.models.unit import Unit
from app.repositories.payments import PaymentRepository
from app.schemas.payment import PaymentCreate
from app.utils.exceptions import NotFoundError


class PaymentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.payments = PaymentRepository(session)

    async def _tenant_for_owner(self, *, owner_id: uuid.UUID, tenant_id: uuid.UUID) -> Tenant | None:
        stmt = (
            select(Tenant)
            .join(Unit, Unit.id == Tenant.unit_id)
            .join(Property, Property.id == Unit.property_id)
            .where(
                Tenant.id == tenant_id,
                Tenant.is_deleted.is_(False),
                Unit.is_deleted.is_(False),
                Property.is_deleted.is_(False),
                Property.owner_id == owner_id,
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_for_tenant(self, *, owner_id: uuid.UUID, tenant_id: uuid.UUID):
        tenant = await self._tenant_for_owner(owner_id=owner_id, tenant_id=tenant_id)
        if not tenant:
            raise NotFoundError("Tenant not found")
        return await self.payments.list_for_tenant(tenant_id)

    async def create(self, *, owner_id: uuid.UUID, payload: PaymentCreate):
        tenant = await self._tenant_for_owner(owner_id=owner_id, tenant_id=payload.tenant_id)
        if not tenant:
            raise NotFoundError("Tenant not found")

        payment = await self.payments.create(
            tenant_id=payload.tenant_id,
            amount=payload.amount,
            payment_date=payload.payment_date,
            status=payload.status,
            note=payload.note,
        )
        await self.session.commit()
        return payment


from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import func, select

from app.models.payment import Payment
from app.repositories.base import BaseRepository


class PaymentRepository(BaseRepository):
    async def get(self, payment_id: uuid.UUID) -> Payment | None:
        stmt = select(Payment).where(Payment.id == payment_id, Payment.is_deleted.is_(False))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_for_tenant(self, tenant_id: uuid.UUID) -> list[Payment]:
        stmt = select(Payment).where(Payment.tenant_id == tenant_id, Payment.is_deleted.is_(False)).order_by(
            Payment.payment_date.desc(), Payment.created_at.desc()
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create(self, *, tenant_id: uuid.UUID, amount, payment_date: date, status: str, note: str | None) -> Payment:
        payment = Payment(tenant_id=tenant_id, amount=amount, payment_date=payment_date, status=status, note=note)
        self.session.add(payment)
        await self.session.flush()
        return payment

    async def sum_received(self, *, tenant_ids: list[uuid.UUID], from_date: date, to_date: date):
        if not tenant_ids:
            return 0, 0
        stmt = (
            select(func.coalesce(func.sum(Payment.amount), 0), func.count(Payment.id))
            .where(
                Payment.is_deleted.is_(False),
                Payment.tenant_id.in_(tenant_ids),
                Payment.payment_date >= from_date,
                Payment.payment_date <= to_date,
                Payment.status == "paid",
            )
            .select_from(Payment)
        )
        res = await self.session.execute(stmt)
        total, count = res.one()
        return total, count

    async def last_payment_date(self, *, tenant_id: uuid.UUID) -> date | None:
        stmt = select(func.max(Payment.payment_date)).where(
            Payment.is_deleted.is_(False), Payment.tenant_id == tenant_id, Payment.status == "paid"
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()


from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property
from app.models.tenant import Tenant
from app.models.unit import Unit
from app.repositories.payments import PaymentRepository
from app.schemas.reports import CollectionSummary, TenantDue


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.payments = PaymentRepository(session)

    async def collection_summary(self, *, owner_id: uuid.UUID, from_date: date, to_date: date) -> CollectionSummary:
        stmt = (
            select(Tenant.id)
            .join(Unit, Unit.id == Tenant.unit_id)
            .join(Property, Property.id == Unit.property_id)
            .where(
                Tenant.is_deleted.is_(False),
                Unit.is_deleted.is_(False),
                Property.is_deleted.is_(False),
                Property.owner_id == owner_id,
            )
        )
        res = await self.session.execute(stmt)
        tenant_ids = [row[0] for row in res.all()]
        total_received, total_payments = await self.payments.sum_received(tenant_ids=tenant_ids, from_date=from_date, to_date=to_date)
        return CollectionSummary(
            from_date=from_date,
            to_date=to_date,
            total_received=Decimal(str(total_received)),
            total_payments=int(total_payments),
        )

    async def pending_dues(self, *, owner_id: uuid.UUID, as_of: date) -> list[TenantDue]:
        # MVP heuristic: if tenant has no "paid" payment in the current month, due ~= monthly rent.
        month_start = as_of.replace(day=1)

        stmt = (
            select(
                Tenant.id,
                Tenant.tenant_name,
                Unit.id,
                Unit.unit_name,
                Property.id,
                Property.property_name,
                Unit.rent_amount,
            )
            .join(Unit, Unit.id == Tenant.unit_id)
            .join(Property, Property.id == Unit.property_id)
            .where(
                Tenant.is_deleted.is_(False),
                Unit.is_deleted.is_(False),
                Property.is_deleted.is_(False),
                Property.owner_id == owner_id,
            )
        )
        res = await self.session.execute(stmt)
        rows = res.all()

        out: list[TenantDue] = []
        for tenant_id, tenant_name, unit_id, unit_name, prop_id, prop_name, rent_amount in rows:
            last_paid = await self.payments.last_payment_date(tenant_id=tenant_id)
            due = Decimal("0")
            if last_paid is None or last_paid < month_start:
                due = Decimal(str(rent_amount))

            out.append(
                TenantDue(
                    tenant_id=tenant_id,
                    tenant_name=tenant_name,
                    unit_id=unit_id,
                    unit_name=unit_name,
                    property_id=prop_id,
                    property_name=prop_name,
                    monthly_rent=Decimal(str(rent_amount)),
                    last_payment_date=last_paid,
                    due_amount_estimate=due,
                )
            )
        return out


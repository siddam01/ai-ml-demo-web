from __future__ import annotations

import uuid

from sqlalchemy import select

from app.models.property import Property
from app.models.unit import Unit
from app.repositories.base import BaseRepository


class PropertyRepository(BaseRepository):
    async def list_for_owner(self, owner_id: uuid.UUID) -> list[Property]:
        stmt = select(Property).where(Property.owner_id == owner_id, Property.is_deleted.is_(False)).order_by(
            Property.created_at.desc()
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_for_owner(self, owner_id: uuid.UUID, property_id: uuid.UUID) -> Property | None:
        stmt = select(Property).where(
            Property.id == property_id,
            Property.owner_id == owner_id,
            Property.is_deleted.is_(False),
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, *, owner_id: uuid.UUID, property_name: str, address: str | None) -> Property:
        prop = Property(owner_id=owner_id, property_name=property_name, address=address)
        self.session.add(prop)
        await self.session.flush()
        return prop

    async def update(self, prop: Property, *, property_name: str | None, address: str | None) -> Property:
        if property_name is not None:
            prop.property_name = property_name
        if address is not None:
            prop.address = address
        await self.session.flush()
        return prop

    async def soft_delete(self, prop: Property) -> None:
        prop.is_deleted = True
        await self.session.flush()


class UnitRepository(BaseRepository):
    async def list_for_property(self, property_id: uuid.UUID) -> list[Unit]:
        stmt = select(Unit).where(Unit.property_id == property_id, Unit.is_deleted.is_(False)).order_by(Unit.created_at.desc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get(self, unit_id: uuid.UUID) -> Unit | None:
        stmt = select(Unit).where(Unit.id == unit_id, Unit.is_deleted.is_(False))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create(self, *, property_id: uuid.UUID, unit_name: str, rent_amount) -> Unit:
        unit = Unit(property_id=property_id, unit_name=unit_name, rent_amount=rent_amount)
        self.session.add(unit)
        await self.session.flush()
        return unit

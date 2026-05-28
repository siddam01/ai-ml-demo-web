from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.properties import PropertyRepository, UnitRepository
from app.schemas.property import PropertyCreate, PropertyUpdate, UnitCreate
from app.utils.exceptions import NotFoundError


class PropertyService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.properties = PropertyRepository(session)
        self.units = UnitRepository(session)

    async def list_properties(self, *, owner_id: uuid.UUID):
        return await self.properties.list_for_owner(owner_id)

    async def create_property(self, *, owner_id: uuid.UUID, payload: PropertyCreate):
        prop = await self.properties.create(owner_id=owner_id, property_name=payload.property_name, address=payload.address)
        await self.session.commit()
        return prop

    async def update_property(self, *, owner_id: uuid.UUID, property_id: uuid.UUID, payload: PropertyUpdate):
        prop = await self.properties.get_for_owner(owner_id, property_id)
        if not prop:
            raise NotFoundError("Property not found")
        await self.properties.update(prop, property_name=payload.property_name, address=payload.address)
        await self.session.commit()
        return prop

    async def delete_property(self, *, owner_id: uuid.UUID, property_id: uuid.UUID):
        prop = await self.properties.get_for_owner(owner_id, property_id)
        if not prop:
            raise NotFoundError("Property not found")
        await self.properties.soft_delete(prop)
        await self.session.commit()

    async def list_units(self, *, owner_id: uuid.UUID, property_id: uuid.UUID):
        prop = await self.properties.get_for_owner(owner_id, property_id)
        if not prop:
            raise NotFoundError("Property not found")
        return await self.units.list_for_property(property_id)

    async def create_unit(self, *, owner_id: uuid.UUID, property_id: uuid.UUID, payload: UnitCreate):
        prop = await self.properties.get_for_owner(owner_id, property_id)
        if not prop:
            raise NotFoundError("Property not found")
        unit = await self.units.create(property_id=property_id, unit_name=payload.unit_name, rent_amount=payload.rent_amount)
        await self.session.commit()
        return unit


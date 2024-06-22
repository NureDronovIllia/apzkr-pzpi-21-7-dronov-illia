from typing import Any, Optional

from sqlalchemy import select

from app.models.db.vehicle import Inspection
from app.repository.base import BaseRepository


class InspectionRepository(BaseRepository):
    model = Inspection

    async def get_inspection(self, inspection_id: int) -> Inspection:
        query = select(Inspection).where(Inspection.id == inspection_id)
        return await self.get_instance(query)

    async def get_current_inspection(self, vehicle_id: int) -> Inspection:
        query = select(Inspection).where(
            (Inspection.vehicle_id == vehicle_id) & (Inspection.end_time == None)
        )
        return await self.get_instance(query)

    async def is_vehicle_on_inspection(self, vehicle_id: int) -> bool:
        inspection = await self.get_current_inspection(vehicle_id)
        return bool(inspection)

    async def get_inspections(self) -> list[Inspection]:
        query = select(Inspection)
        return self.unpack(await self.get_many(query))

    async def create_inspection(
        self, inspection_data, *args, **kwargs
    ) -> dict[str, Any]:
        new_inspection: Inspection = await self.create(inspection_data, **kwargs)
        return new_inspection

    async def update_inspection(
        self, inspection_id: int, inspection_data
    ) -> Inspection:
        updated_user = await self.update(inspection_id, inspection_data)
        return updated_user

from typing import Any, Optional

from sqlalchemy import select

from app.models.db.vehicle import Status, Vehicle, VehicleStatuses
from app.models.schemas.vehicle import SetStatus
from app.repository.base import BaseRepository


class VehicleRepository(BaseRepository):
    model = Vehicle

    async def get_vehicle(self, vehicle_id: int) -> Vehicle:
        query = select(Vehicle).where(Vehicle.id == vehicle_id)
        return await self.get_instance(query)

    async def get_vehicles(self) -> list[Vehicle]:
        query = select(Vehicle)
        return self.unpack(await self.get_many(query))

    async def get_recent_status(self, vehicle_id: int) -> VehicleStatuses:
        query = (
            select(Status.status)
            .where(Status.vehicle_id == vehicle_id)
            .order_by(Status.created_at.desc())
            .limit(2)
        )
        statuses: list[VehicleStatuses] = self.unpack(await self.get_many(query))
        return statuses[1]

    async def get_current_status(self, vehicle_id: int) -> VehicleStatuses:
        query = (
            select(Status.status)
            .where(Status.vehicle_id == vehicle_id)
            .order_by(Status.created_at.desc())
            .limit(1)
        )
        return await self.get_instance(query)

    async def set_current_status(
        self, vehicle_id: int, status: VehicleStatuses
    ) -> None:
        new_status = Status(vehicle_id=vehicle_id, status=status)
        self.async_session.add(new_status)
        await self.async_session.commit()

    async def create_vehicle(self, vehicle_data) -> dict[str, Any]:
        new_vehicle: Vehicle = await self.create(vehicle_data)
        await self.set_current_status(new_vehicle.id, VehicleStatuses.OFF_SHIFT)
        return new_vehicle

    async def update_vehicle(self, vehicle_id: int, vehicle_data) -> Vehicle:
        updated_shift = await self.update(vehicle_id, vehicle_data)
        return updated_shift

    async def delete_vehicle(self, user_id: int) -> Optional[int]:
        result = await self.delete(user_id)
        return result

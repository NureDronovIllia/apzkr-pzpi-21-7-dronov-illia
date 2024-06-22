from typing import Any, Optional

from sqlalchemy import select

from app.models.db.fuel import FuelStorage
from app.repository.base import BaseRepository


class FuelStorageRepository(BaseRepository):
    model = FuelStorage

    async def get_fuel_storage(self, fuel_storage_id: int) -> FuelStorage:
        query = select(FuelStorage).where(FuelStorage.id == fuel_storage_id)
        return await self.get_instance(query)

    async def get_fuel_storages(self) -> list[FuelStorage]:
        query = select(FuelStorage)
        return self.unpack(await self.get_many(query))

    async def create_fuel_storage(self, fuel_storage_data) -> dict[str, Any]:
        new_fuel_storage: FuelStorage = await self.create(fuel_storage_data)
        return new_fuel_storage

    async def update_fuel_storage(
        self, fuel_storage_id: int, fuel_storage_data
    ) -> FuelStorage:
        updated_fuel_storage = await self.update(fuel_storage_id, fuel_storage_data)
        return updated_fuel_storage

    async def delete_fuel_storage(self, fuel_storage_id: int) -> Optional[int]:
        result = await self.delete(fuel_storage_id)
        return result

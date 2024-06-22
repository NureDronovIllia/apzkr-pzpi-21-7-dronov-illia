from typing import Any, Optional

from sqlalchemy import select

from app.models.db.fuel import FuelSupplier
from app.repository.base import BaseRepository


class FuelSupplierRepository(BaseRepository):
    model = FuelSupplier

    async def get_fuel_supplier(self, fuel_supplier_id: int) -> FuelSupplier:
        query = select(FuelSupplier).where(FuelSupplier.id == fuel_supplier_id)
        return await self.get_instance(query)

    async def get_fuel_suppliers(self) -> list[FuelSupplier]:
        query = select(FuelSupplier)
        return self.unpack(await self.get_many(query))

    async def create_fuel_supplier(self, fuel_supplier_data) -> dict[str, Any]:
        new_fuel_supplier: FuelSupplier = await self.create(fuel_supplier_data)
        return new_fuel_supplier

    async def update_fuel_supplier(
        self, fuel_supplier_id: int, fuel_supplier_data
    ) -> FuelSupplier:
        updated_fuel_supplier = await self.update(fuel_supplier_id, fuel_supplier_data)
        return updated_fuel_supplier

    async def delete_fuel_supplier(self, fuel_supplier_id: int) -> Optional[int]:
        result = await self.delete(fuel_supplier_id)
        return result

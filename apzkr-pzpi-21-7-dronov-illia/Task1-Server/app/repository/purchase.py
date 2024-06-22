from typing import Any, Optional

from sqlalchemy import select

from app.models.db.fuel import Purchase
from app.repository.base import BaseRepository


class PurchaseRepository(BaseRepository):
    model = Purchase

    async def get_purchase(self, purchase_id: int) -> Purchase:
        query = select(Purchase).where(Purchase.id == purchase_id)
        return await self.get_instance(query)

    async def get_purchases(self) -> list[Purchase]:
        query = select(Purchase)
        return self.unpack(await self.get_many(query))

    async def create_purchase(self, purchase_data) -> dict[str, Any]:
        new_purchase: Purchase = await self.create(purchase_data)
        return new_purchase

    async def update_purchase(self, purchase_id: int, purchase_data) -> Purchase:
        updated_purchase = await self.update(purchase_id, purchase_data)
        return updated_purchase

    async def delete_purchase(self, purchase_id: int) -> Optional[int]:
        result = await self.delete(purchase_id)
        return result

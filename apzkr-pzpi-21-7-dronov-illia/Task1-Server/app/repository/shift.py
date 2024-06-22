from typing import Any

from sqlalchemy import select

from app.models.db.shift import Shift
from app.repository.base import BaseRepository


class ShiftRepository(BaseRepository):
    model = Shift

    async def get_shift(self, shift_id: int) -> Shift:
        query = select(Shift).where(Shift.id == shift_id)
        return await self.get_instance(query)

    async def get_current_user_shift(self, user_id: int) -> Shift:
        query = select(Shift).where(
            (Shift.user_id == user_id) & (Shift.end_time == None)
        )
        return await self.get_instance(query)

    async def get_shifts(self) -> list[Shift]:
        query = select(Shift)
        return self.unpack(await self.get_many(query))

    async def create_shift(self, shift_data) -> dict[str, Any]:
        new_shift: Shift = await self.create(shift_data)
        return new_shift

    async def update_shift(self, shift_id: int, shift_data) -> Shift:
        updated_shift = await self.update(shift_id, shift_data)
        return updated_shift

    async def is_user_on_shift(self, user_id: int) -> bool:
        shift: Shift = await self.get_current_user_shift(user_id)
        return bool(shift)

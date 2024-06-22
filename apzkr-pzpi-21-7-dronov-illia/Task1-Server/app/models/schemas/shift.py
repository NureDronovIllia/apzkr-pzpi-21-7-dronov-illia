from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ShiftBase(BaseModel):
    vehicle_id: int


class ShiftData(ShiftBase):
    id: int
    user_id: int
    vehicle_id: int
    start_time: datetime
    end_time: Optional[datetime] = None


class ShiftCreate(ShiftBase):
    user_id: int


class ShiftUpdate(BaseModel):
    end_time: datetime

from datetime import datetime
from typing import Annotated, Optional

from annotated_types import Ge, Gt, Le
from pydantic import BaseModel, field_validator

from app.models.db.vehicle import VehicleStatuses, VehicleTypes
from app.utilities.validators.payload.user import validate_name


class VehicleBase(BaseModel):
    type: VehicleTypes
    title: str
    current_fuel_lvl: Optional[Annotated[float, Ge(0)]] = 0
    max_fuel_lvl: Annotated[float, Gt(0)]
    current_lng: Annotated[float, Ge(-180), Le(180)]
    current_lat: Annotated[float, Ge(-90), Le(90)]


class VehicleData(VehicleBase):
    id: int
    current_status: Optional[str]


class SetStatus(BaseModel):
    status: VehicleStatuses


class RefuelData(BaseModel):
    amount: float


class VehicleUpdate(BaseModel):
    current_fuel_lvl: Optional[Annotated[float, Ge(0)]] = None
    current_lng: Optional[Annotated[float, Ge(-180), Le(180)]] = None
    current_lat: Optional[Annotated[float, Ge(-90), Le(90)]] = None


class InspectionBase(BaseModel):
    vehicle_id: int
    reason: str


class InspectionData(InspectionBase):
    id: int
    conclusion: Optional[str] = None
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None


class InspectionUpdate(BaseModel):
    conclusion: Optional[str] = None
    reason: Optional[str] = None
    end_time: Optional[datetime] = None

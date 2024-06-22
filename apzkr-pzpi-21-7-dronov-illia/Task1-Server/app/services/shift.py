from datetime import datetime

from fastapi import HTTPException, status

from app.models.db.shift import Shift
from app.models.db.user import User, UserRoles
from app.models.db.vehicle import VehicleStatuses
from app.models.schemas.shift import ShiftBase, ShiftCreate, ShiftData, ShiftUpdate
from app.repository.shift import ShiftRepository
from app.repository.user import UserRepository
from app.repository.vehicle import VehicleRepository
from app.services.base import BaseService
from app.utilities.formatters.http_error import error_wrapper


class ShiftService(BaseService):
    def __init__(self, user_repository, shift_repository, vehicle_repository) -> None:
        self.user_repository: UserRepository = user_repository
        self.shift_repository: ShiftRepository = shift_repository
        self.vehicle_repository: VehicleRepository = vehicle_repository

    async def get_shifts(self, current_user: User) -> list[ShiftData]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        shifts = await self.shift_repository.get_shifts()
        return [ShiftData(**shift.__dict__) for shift in shifts]

    async def start_shift(self, shift_data: ShiftBase, current_user: User) -> ShiftData:
        await self._validate_user_permissions(
            self.user_repository, current_user.id, UserRoles.EMPLOYEE
        )
        await self._validate_instance_exists(
            self.vehicle_repository, shift_data.vehicle_id
        )

        current_vehicle_status: VehicleStatuses = (
            await self.vehicle_repository.get_current_status(shift_data.vehicle_id)
        )
        if current_vehicle_status != VehicleStatuses.OFF_SHIFT:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                error_wrapper("You can't use this vehicle at the moment", "vehicle_id"),
            )

        user_on_shift: bool = await self.shift_repository.is_user_on_shift(
            current_user.id
        )
        if user_on_shift:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "You are currently on the shift",
            )

        vehicle_id: int = shift_data.vehicle_id
        new_shift: Shift = await self.shift_repository.create_shift(
            ShiftCreate(vehicle_id=vehicle_id, user_id=current_user.id)
        )

        await self.vehicle_repository.set_current_status(
            vehicle_id, VehicleStatuses.SHIFT
        )

        return ShiftData(**new_shift.__dict__)

    async def end_shift(self, shift_id: int, current_user: User) -> ShiftData:
        await self._validate_user_permissions(
            self.user_repository, current_user.id, UserRoles.EMPLOYEE
        )
        await self._validate_instance_exists(self.shift_repository, shift_id)

        shift: Shift = await self.shift_repository.get_shift(shift_id)
        if shift.end_time:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "This shift is already ended up"
            )

        if shift.user_id != current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Forbidden")

        updated_shift = await self.shift_repository.update_shift(
            shift_id, (ShiftUpdate(end_time=datetime.utcnow()))
        )
        await self.vehicle_repository.set_current_status(
            updated_shift.vehicle_id, VehicleStatuses.OFF_SHIFT
        )

        return updated_shift

from fastapi import HTTPException, status

from app.models.db.shift import Shift
from app.models.db.user import User, UserRoles
from app.models.db.vehicle import Inspection, Vehicle, VehicleStatuses
from app.models.schemas.vehicle import (
    InspectionBase,
    InspectionData,
    InspectionUpdate,
    RefuelData,
    SetStatus,
    VehicleBase,
    VehicleData,
    VehicleUpdate,
)
from app.repository.inspection import InspectionRepository
from app.repository.shift import ShiftRepository
from app.repository.user import UserRepository
from app.repository.vehicle import VehicleRepository
from app.services.base import BaseService


class VehicleService(BaseService):
    def __init__(
        self,
        user_repository,
        vehicle_repository,
        shift_repository,
        inspection_repository,
    ) -> None:
        self.user_repository: UserRepository = user_repository
        self.vehicle_repository: VehicleRepository = vehicle_repository
        self.shift_repository: ShiftRepository = shift_repository
        self.inspection_repository: InspectionRepository = inspection_repository

    async def _get_vehicles_with_status(
        self, vehicles: list[Vehicle]
    ) -> list[VehicleData]:
        current_statuses: list[str] = [
            await self.vehicle_repository.get_current_status(vehicle.id)
            for vehicle in vehicles
        ]

        # Unpack main vehicle object and add a status field
        return [
            VehicleData(
                **vehicle.__dict__,
                current_status=VehicleStatuses(status) if status else None,
            )
            for vehicle, status in zip(vehicles, current_statuses)
        ]

    async def get_vehicles(self, current_user: User) -> list[VehicleData]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        vehicles: list[Vehicle] = await self.vehicle_repository.get_vehicles()
        return await self._get_vehicles_with_status(vehicles)

    async def refuel_vehicle(
        self, vehicle_id: int, data: RefuelData, current_user: User
    ) -> None:
        await self._validate_instance_exists(self.vehicle_repository, vehicle_id)
        await self._validate_user_permissions(
            self.user_repository, current_user.id, UserRoles.EMPLOYEE
        )

        vehicle: Vehicle = await self.vehicle_repository.get_vehicle(vehicle_id)
        vehicle_status = await self.vehicle_repository.get_current_status(vehicle_id)
        if vehicle_status in [VehicleStatuses.FUEL, VehicleStatuses.INSPECTION]:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "You can't refuel this vehicle at the moment",
            )

        if vehicle_status != VehicleStatuses.OFF_SHIFT:
            # Validate if employee can access the vehicle
            current_shift: Shift = await self.shift_repository.get_current_user_shift(
                current_user.id
            )
            if not current_shift or current_shift.vehicle_id != vehicle_id:
                raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Forbidden")

        allowed_fuel_amount: float = round(
            vehicle.max_fuel_lvl - vehicle.current_fuel_lvl
        )
        if data.amount > allowed_fuel_amount:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"You can't put that much fuel in. Maximum permissible value is {allowed_fuel_amount}",
            )

        await self.vehicle_repository.set_current_status(
            vehicle_id, VehicleStatuses.FUEL
        )
        vehicle.current_fuel_lvl += data.amount
        await self.vehicle_repository.save(vehicle)

    async def stop_refuel(self, vehicle_id: int, current_user: User) -> None:
        await self._validate_instance_exists(self.vehicle_repository, vehicle_id)
        await self._validate_user_permissions(
            self.user_repository, current_user.id, UserRoles.EMPLOYEE
        )

        vehicle_status = await self.vehicle_repository.get_current_status(vehicle_id)
        if vehicle_status != VehicleStatuses.FUEL:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "The vehicle is not on a refuel"
            )

        # Set status that was before refueling
        recent_status = await self.vehicle_repository.get_recent_status(vehicle_id)
        await self.vehicle_repository.set_current_status(vehicle_id, recent_status)

    async def create_vehicle(
        self, data: VehicleBase, current_user: User
    ) -> VehicleData:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        new_vehicle: Vehicle = await self.vehicle_repository.create_vehicle(data)
        return (await self._get_vehicles_with_status([new_vehicle]))[0]

    async def set_current_status(
        self, vehicle_id: int, status: SetStatus, current_user: User
    ) -> None:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.vehicle_repository, vehicle_id)

        await self.vehicle_repository.set_current_status(vehicle_id, status.status)

    async def update_vehicle(
        self, vehicle_id: int, data: VehicleUpdate, current_user: User
    ) -> VehicleData:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.vehicle_repository, vehicle_id)

        updated_vehicle: Vehicle = await self.vehicle_repository.update_vehicle(
            vehicle_id, data
        )
        return (await self._get_vehicles_with_status([updated_vehicle]))[0]

    async def delete_vehicle(self, vehicle_id: int, current_user: User) -> None:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.vehicle_repository, vehicle_id)

        await self.vehicle_repository.delete_vehicle(vehicle_id)

    async def get_inspections(self, current_user: User) -> list[VehicleData]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        inspections: list[
            Inspection
        ] = await self.inspection_repository.get_inspections()
        return [InspectionData(**inspection.__dict__) for inspection in inspections]

    async def start_inspection(
        self, data: InspectionBase, current_user: User
    ) -> InspectionData:
        await self._validate_instance_exists(self.vehicle_repository, data.vehicle_id)
        await self._validate_user_permissions(
            self.user_repository, current_user.id, UserRoles.EMPLOYEE
        )

        # Validate if employee can access the vehicle
        current_shift: Shift = await self.shift_repository.get_current_user_shift(
            current_user.id
        )
        if not current_shift or current_shift.vehicle_id != data.vehicle_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Forbidden")

        is_vehicle_on_inspection: bool = (
            await self.inspection_repository.is_vehicle_on_inspection(data.vehicle_id)
        )
        if is_vehicle_on_inspection:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "This vehicle is already on inspection"
            )

        inspection: Inspection = await self.inspection_repository.create_inspection(
            data, user_id=current_user.id
        )

        await self.vehicle_repository.set_current_status(
            data.vehicle_id, VehicleStatuses.INSPECTION
        )
        return InspectionData(**inspection.__dict__)

    async def end_inspection(
        self, inspection_id: int, data: InspectionUpdate, current_user: User
    ) -> InspectionData:
        await self._validate_instance_exists(self.inspection_repository, inspection_id)
        await self._validate_user_permissions(
            self.user_repository, current_user.id, UserRoles.EMPLOYEE
        )

        inspection: Inspection = await self.inspection_repository.get_inspection(
            inspection_id
        )
        if inspection.user_id != current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

        if inspection.end_time:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "This inspection is already over"
            )

        updated_inspection: Inspection = (
            await self.inspection_repository.update_inspection(inspection_id, data)
        )
        await self.vehicle_repository.set_current_status(
            updated_inspection.vehicle_id, VehicleStatuses.OFF_SHIFT
        )

        return InspectionData(**updated_inspection.__dict__)

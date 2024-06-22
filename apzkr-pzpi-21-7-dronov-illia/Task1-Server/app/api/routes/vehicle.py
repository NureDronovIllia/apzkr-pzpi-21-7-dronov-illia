from fastapi import APIRouter, Depends

from app.api.dependencies.services import get_vehicle_service
from app.api.dependencies.user import get_current_user
from app.models.db.user import User
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
from app.services.vehicle import VehicleService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.get("/", response_model=list[VehicleData])
async def get_vehicles(
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> list[VehicleData]:
    return await vehicle_service.get_vehicles(current_user)


@router.post("/refuel/", response_model=None, status_code=201)
async def refuel_vehicle(
    vehicle_id: int,
    data: RefuelData,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> None:
    await vehicle_service.refuel_vehicle(vehicle_id, data, current_user)


@router.post("/refuel/stop/", response_model=None, status_code=201)
async def refuel_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> None:
    await vehicle_service.stop_refuel(vehicle_id, current_user)


@router.post("/{vehicle_id}/set_current_status/", response_model=None, status_code=201)
async def set_current_status(
    vehicle_id: int,
    status: SetStatus,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> None:
    return await vehicle_service.set_current_status(vehicle_id, status, current_user)


@router.post("/create/", response_model=VehicleData, status_code=201)
async def create_vehicle(
    data: VehicleBase,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> VehicleData:
    return await vehicle_service.create_vehicle(data, current_user)


@router.patch("/{vehicle_id}/update/", response_model=VehicleData)
async def update_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> VehicleData:
    return await vehicle_service.update_vehicle(vehicle_id, data, current_user)


@router.delete("/{vehicle_id}/delete/", response_model=None, status_code=204)
async def delete_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> None:
    return await vehicle_service.delete_vehicle(vehicle_id, current_user)


@router.get("/inspections/", response_model=list[InspectionData])
async def get_inspections(
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> list[InspectionData]:
    return await vehicle_service.get_inspections(current_user)


@router.post("/inspections/start/", response_model=InspectionData)
async def start_inspection(
    data: InspectionBase,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> InspectionData:
    return await vehicle_service.start_inspection(data, current_user)


@router.post("/inspections/{inspection_id}/end/", response_model=InspectionData)
async def end_inspection(
    inspection_id: int,
    data: InspectionUpdate,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service),
) -> InspectionData:
    return await vehicle_service.end_inspection(inspection_id, data, current_user)

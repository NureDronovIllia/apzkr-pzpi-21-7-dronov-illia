from fastapi import APIRouter, Depends

from app.api.dependencies.services import get_fuel_service
from app.api.dependencies.user import get_current_user
from app.models.db.user import User
from app.models.schemas.fuel import (
    PurchaseBase,
    PurchaseData,
    StorageBase,
    StorageData,
    StorageUpdate,
    SupplierBase,
    SupplierData,
    SupplierUpdate,
)
from app.services.fuel import FuelService

router = APIRouter(prefix="/fuel", tags=["Fuel"])


@router.get("/suppliers/", response_model=list[SupplierData])
async def get_suppliers(
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> list[SupplierData]:
    return await fuel_service.get_suppliers(current_user)


@router.post("/suppliers/", response_model=SupplierData, status_code=201)
async def create_supplier(
    data: SupplierBase,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> SupplierData:
    return await fuel_service.create_supplier(data, current_user)


@router.patch("/suppliers/{supplier_id}/update/", response_model=SupplierData)
async def update_supplier(
    data: SupplierUpdate,
    supplier_id: int,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> SupplierData:
    return await fuel_service.update_supplier(data, supplier_id, current_user)


@router.delete("/suppliers/{supplier_id}/delete/", response_model=None, status_code=204)
async def delete_supplier(
    supplier_id: int,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> None:
    return await fuel_service.delete_supplier(supplier_id, current_user)


@router.get("/storages/", response_model=list[StorageData])
async def get_storages(
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> list[StorageData]:
    return await fuel_service.get_storages(current_user)


@router.post("/storages/", response_model=StorageData, status_code=201)
async def create_storage(
    data: StorageBase,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> StorageData:
    return await fuel_service.create_storage(data, current_user)


@router.patch("/storages/{storage_id}/update/", response_model=StorageData)
async def update_storage(
    data: StorageUpdate,
    storage_id: int,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> StorageData:
    return await fuel_service.update_storage(storage_id, data, current_user)


@router.delete("/storages/{storage_id}/delete/", response_model=None, status_code=204)
async def delete_storage(
    storage_id: int,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> None:
    return await fuel_service.delete_storage(storage_id, current_user)


@router.get("/pucrhases/", response_model=list[PurchaseData])
async def get_purchases(
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> list[PurchaseData]:
    return await fuel_service.get_purchases(current_user)


@router.post("/purchases/", response_model=PurchaseData, status_code=201)
async def create_purchase(
    data: PurchaseBase,
    current_user: User = Depends(get_current_user),
    fuel_service: FuelService = Depends(get_fuel_service),
) -> PurchaseData:
    return await fuel_service.create_purchase(data, current_user)
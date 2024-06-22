from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.db.fuel import FuelStorage, FuelSupplier, Purchase
from app.models.db.user import User
from app.models.schemas.fuel import (
    PurchaseBase,
    PurchaseCreate,
    PurchaseData,
    StorageBase,
    StorageData,
    StorageUpdate,
    SupplierBase,
    SupplierData,
    SupplierUpdate,
)
from app.repository.fuel_storage import FuelStorageRepository
from app.repository.fuel_supplier import FuelSupplierRepository
from app.repository.purchase import PurchaseRepository
from app.repository.user import UserRepository
from app.services.base import BaseService
from app.utilities.formatters.http_error import error_wrapper


class FuelService(BaseService):
    def __init__(
        self,
        user_repository,
        fuel_supplier_repository,
        fuel_storage_repository,
        purchase_repository,
    ) -> None:
        self.user_repository: UserRepository = user_repository
        self.fuel_supplier_repository: FuelSupplierRepository = fuel_supplier_repository
        self.fuel_storage_repository: FuelStorageRepository = fuel_storage_repository
        self.purchase_repository: PurchaseRepository = purchase_repository

    async def get_suppliers(self, current_user: User) -> list[SupplierData]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        suppliers = await self.fuel_supplier_repository.get_fuel_suppliers()
        return [SupplierData(**supplier.__dict__) for supplier in suppliers]

    async def create_supplier(
        self, data: SupplierBase, current_user: User
    ) -> SupplierData:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        try:
            new_supplier: FuelSupplier = (
                await self.fuel_supplier_repository.create_fuel_supplier(data)
            )
            return SupplierData(**new_supplier.__dict__)
        except IntegrityError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=error_wrapper(
                    "Fuel supplier with this title already exists", "title"
                ),
            )

    async def update_supplier(
        self, supplier_id: int, data: SupplierUpdate, current_user: User
    ) -> SupplierData:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.fuel_supplier_repository, supplier_id)

        try:
            updated_supplier: FuelSupplier = (
                await self.fuel_supplier_repository.update_fuel_supplier(
                    supplier_id, data
                )
            )
            return SupplierData(**updated_supplier.__dict__)
        except IntegrityError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=error_wrapper(
                    "Fuel supplier with this title already exists", "title"
                ),
            )

    async def delete_supplier(self, supplier_id: int, current_user: User) -> None:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.fuel_supplier_repository, supplier_id)

        await self.fuel_supplier_repository.delete_fuel_supplier(supplier_id)

    async def get_storages(self, current_user: User) -> list[StorageData]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        storages = await self.fuel_storage_repository.get_fuel_storages()
        return [StorageData(**storage.__dict__) for storage in storages]

    async def create_storage(
        self, data: StorageBase, current_user: User
    ) -> StorageData:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        new_storage: FuelStorage = (
            await self.fuel_storage_repository.create_fuel_storage(data)
        )
        return StorageData(**new_storage.__dict__)

    async def update_storage(
        self, storage_id: int, data: StorageUpdate, current_user: User
    ) -> SupplierData:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.fuel_storage_repository, storage_id)

        updated_storage: FuelStorage = (
            await self.fuel_storage_repository.update_fuel_storage(storage_id, data)
        )
        return StorageData(**updated_storage.__dict__)

    async def delete_storage(self, storage_id: int, current_user: User) -> None:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.fuel_storage_repository, storage_id)

        await self.fuel_storage_repository.delete_fuel_storage(storage_id)

    async def get_purchases(self, current_user: User) -> list[PurchaseData]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        purchases = await self.purchase_repository.get_purchases()
        return [PurchaseData(**purchase.__dict__) for purchase in purchases]

    async def create_purchase(
        self, data: PurchaseBase, current_user: User
    ) -> PurchaseData:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        fuel_storage: FuelStorage = await self.fuel_storage_repository.get_fuel_storage(
            data.fuel_storage_id
        )

        fuel_supplier: FuelSupplier = await self.fuel_supplier_repository.get_fuel_supplier(data.fuel_supplier_id)
        if fuel_supplier.fuel_type != fuel_storage.fuel_type:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Type of fuel doesn't match for the storage and supplier")

        allowed_amount: float = fuel_storage.max_amount - fuel_storage.current_amount
        if data.amount > allowed_amount:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"You can't put that much fuel in. Maximum permissible value is {allowed_amount}",
            )

        fuel_storage.current_amount += data.amount
        await self.fuel_storage_repository.save(fuel_storage)
        
        new_purchase: Purchase = await self.purchase_repository.create_purchase(
            PurchaseCreate(**data.model_dump(), user_id=current_user.id)
        )
        print(new_purchase)
        return PurchaseData(**new_purchase.__dict__)

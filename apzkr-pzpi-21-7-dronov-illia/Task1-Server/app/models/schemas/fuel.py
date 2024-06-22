from typing import Optional

from pydantic import BaseModel

from app.models.db.fuel import FuelTypes


class SupplierBase(BaseModel):
    title: str
    price: float
    fuel_type: FuelTypes


class SupplierData(SupplierBase):
    id: int


class SupplierUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    fuel_type: Optional[FuelTypes] = None


class StorageBase(BaseModel):
    max_amount: int
    critical_amount: float
    fuel_type: FuelTypes


class StorageData(StorageBase):
    id: int
    current_amount: float


class StorageUpdate(BaseModel):
    max_amount: Optional[int] = None
    current_amount: Optional[float] = None
    critical_amount: Optional[float] = None
    fuel_type: Optional[FuelTypes] = None


class PurchaseBase(BaseModel):
    fuel_storage_id: int
    fuel_supplier_id: int
    amount: float


class PurchaseCreate(PurchaseBase):
    user_id: int


class PurchaseData(PurchaseBase):
    id: int

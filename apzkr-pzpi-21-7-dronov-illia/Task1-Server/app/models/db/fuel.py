import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class FuelTypes(enum.Enum):
    DIESEL = "diesel"
    PETROL = "petrol"
    GAS = "gas"


class FuelStorage(Base):
    __tablename__ = "fuel_storages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    max_amount: Mapped[int]
    current_amount: Mapped[float] = mapped_column(default=0)
    critical_amount: Mapped[float]
    fuel_type: Mapped[FuelTypes] = mapped_column(
        Enum(
            FuelTypes,
            name="fueltypes",
            create_constraint=True,
            validate_strings=True,
        )
    )


class FuelSupplier(Base):
    __tablename__ = "fuel_suppliers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]
    fuel_type: Mapped[FuelTypes] = mapped_column(
        Enum(
            FuelTypes,
            name="fueltypes",
            create_constraint=True,
            validate_strings=True,
        )
    )


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fuel_storage_id: Mapped[int] = mapped_column(
        ForeignKey("fuel_storages.id", ondelete="CASCADE")
    )
    fuel_supplier_id: Mapped[int] = mapped_column(
        ForeignKey("fuel_suppliers.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    amount: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

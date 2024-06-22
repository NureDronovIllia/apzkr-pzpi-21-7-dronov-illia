import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class VehicleTypes(enum.Enum):
    TRUCK = "Truck"
    TRACTOR = "Tractor"
    HARVESTER = "Harvester"
    GENERATOR = "Generator"


class VehicleStatuses(enum.Enum):
    SHIFT = "On the shift"
    INSPECTION = "At the inspection"
    FUEL = "On the refuel"
    OFF_SHIFT = "Off shift"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[VehicleTypes] = mapped_column(
        Enum(
            VehicleTypes,
            name="vehicletypes",
            create_constraint=True,
            validate_strings=True,
        )
    )
    title: Mapped[str] = mapped_column(String(50))
    current_fuel_lvl: Mapped[float] = mapped_column(default=0)
    max_fuel_lvl: Mapped[float]
    current_lng: Mapped[float]
    current_lat: Mapped[float]


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE")
    )
    status: Mapped[VehicleStatuses] = mapped_column(
        Enum(
            VehicleStatuses,
            name="vehiclestatuses",
            create_constraint=True,
            validate_strings=True,
        )
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    reason: Mapped[str]
    conclusion: Mapped[str] = mapped_column(nullable=True)
    start_time: Mapped[datetime] = mapped_column(default=func.now())
    end_time: Mapped[datetime] = mapped_column(nullable=True)

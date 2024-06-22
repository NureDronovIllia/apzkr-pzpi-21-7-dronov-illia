from pathlib import Path
from typing import Any, Dict, Optional

import xlsxwriter
from pydantic import EmailStr
from sqlalchemy import inspect, select

from app.models.db.user import User
from app.models.db.fuel import FuelStorage, FuelSupplier, Purchase
from app.models.db.shift import Shift
from app.models.db.vehicle import Vehicle, Status, Inspection
from app.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    async def get_users(self) -> list[User]:
        query = select(User)
        return self.unpack(await self.get_many(query))

    async def create_user(self, user_data) -> Dict[str, Any]:
        new_user: User = await self.create(user_data)
        return new_user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result: Optional[User] = await self.get_instance(query)
        return result

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        query = select(User).where(User.email == email)
        result: Optional[User] = await self.get_instance(query)
        return result

    async def get_user_id(self, email: EmailStr) -> Optional[int]:
        query = select(User).where(User.email == email).with_only_columns(User.id)
        result: Optional[User] = await self.get_instance(query)
        return result

    async def exists_by_email(self, email: EmailStr) -> bool:
        query = select(User).where(User.email == email)
        return await self.exists(query)

    async def update_user(self, user_id: int, user_data) -> User:
        updated_user = await self.update(user_id, user_data)
        return updated_user

    async def delete_user(self, user_id: int) -> Optional[int]:
        result = await self.delete(user_id)
        return result

    async def export_data_xlsx(self):
        models: list = [
            User,
            FuelStorage,
            FuelSupplier,
            Purchase,
            Shift,
            Vehicle,
            Status,
            Inspection,
        ]
        workbook = xlsxwriter.Workbook(Path("export.xlsx").absolute())

        for model in models:
            worksheet = workbook.add_worksheet(model.__name__)

            # Get all model rows
            query = select(model)
            data = self.unpack(await self.get_many(query))

            # Get table columns' names
            inspector = inspect(model.__table__)
            column_names = [column.name for column in inspector.columns]

            # Fill up the columns
            bold_format = workbook.add_format({"bold": True})
            column = 0
            for item in column_names:
                worksheet.write(0, column, item, bold_format)

                column += 1
            row = 1

            # Fill up the rows
            for data_row in data:
                column = 0
                for column_name in column_names:
                    worksheet.write(row, column, str(getattr(data_row, column_name)))
                    column += 1
                row += 1

        workbook.close()
        return Path("export.xlsx").absolute()

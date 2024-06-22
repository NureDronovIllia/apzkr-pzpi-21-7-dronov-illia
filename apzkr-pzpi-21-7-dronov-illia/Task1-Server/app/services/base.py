from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel

from app.config.logs.logger import logger
from app.models.db.user import UserRoles
from app.repository.base import BaseRepository
from app.repository.user import UserRepository
from app.utilities.formatters.http_error import error_wrapper


class BaseService:
    async def _validate_instance_exists(
        self, repository: BaseRepository, instance_id: int
    ) -> None:
        if not await repository.exists_by_id(instance_id):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"{repository.model.__name__} is not found",
            )

    def _validate_update_data(self, update_data: BaseModel) -> None:
        new_fields: dict = update_data.model_dump(exclude_none=True)
        if new_fields == {}:
            logger.warning("Validation error: No parameters have been provided")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=error_wrapper(
                    "At least one valid field should be provided", None
                ),
            )

    async def _validate_user_permissions(
        self,
        user_repository: UserRepository,
        user_id: int,
        role: Optional[UserRoles] = UserRoles.ADMIN,
        raise_exception: bool = True,
    ) -> None:
        user = await user_repository.get_user_by_id(user_id)
        if user.role != role and raise_exception:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Forbidden")

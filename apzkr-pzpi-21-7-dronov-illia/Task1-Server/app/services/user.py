from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.models.db.user import User, UserRoles
from app.models.schemas.users import (
    PasswordChangeInput,
    PasswordChangeOutput,
    UserData,
    UserLoginInput,
    UserLoginOutput,
    UserRegister,
    UserUpdate,
)
from app.repository.user import UserRepository
from app.securities.authorization.auth_handler import auth_handler
from app.services.base import BaseService
from app.utilities.formatters.http_error import error_wrapper


class UserService(BaseService):
    def __init__(self, user_repository) -> None:
        self.user_repository: UserRepository = user_repository

    async def get_profile(self, current_user) -> UserData:
        return UserData(**current_user.__dict__)

    async def register_user(
        self, user_data: UserRegister, current_user: User
    ) -> UserData:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        # Hashing input password
        user_data.password = auth_handler.get_password_hash(user_data.password)

        try:
            result: User = await self.user_repository.create_user(user_data)
        except IntegrityError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=error_wrapper("User with this email already exists", "email"),
            )

        return UserData(**result.__dict__)

    async def authenticate_user(self, user_data: UserLoginInput) -> UserLoginOutput:
        user_existing_object: User = await self.user_repository.get_user_by_email(
            user_data.email
        )
        if not user_existing_object:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="User with this email is not registered in the system",
            )

        verify_password = auth_handler.verify_password(
            user_data.password, user_existing_object.password
        )
        if not verify_password:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=error_wrapper("Invalid password", "password"),
            )

        auth_token = auth_handler.encode_token(user_existing_object.id, user_data.email)
        return {"token": auth_token}

    async def get_users(self, current_user: User) -> list[User]:
        await self._validate_user_permissions(self.user_repository, current_user.id)

        users: list[User] = await self.user_repository.get_users()
        return [UserData(**user.__dict__) for user in users]

    async def update_user(
        self, user_id: int, user_data: UserUpdate, current_user: User
    ) -> UserData:
        await self._validate_instance_exists(self.user_repository, user_id)
        if user_id != current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

        try:
            updated_user: User = await self.user_repository.update_user(
                user_id, user_data
            )
            return UserData(**updated_user.__dict__)
        except IntegrityError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=error_wrapper("User with this email already exists", "email"),
            )

    async def delete_user(self, user_id: int, current_user: User) -> None:
        await self._validate_user_permissions(self.user_repository, current_user.id)
        await self._validate_instance_exists(self.user_repository, user_id)
        if user_id == current_user.id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "You are trying to delete an account you're currently logged in",
            )

        await self.user_repository.delete_user(user_id)

    async def change_password(
        self, current_user: User, data: PasswordChangeInput
    ) -> PasswordChangeOutput:
        # Validate the old password match the current one
        if not auth_handler.verify_password(data.old_password, current_user.password):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=error_wrapper("Invalid old password", "old_password"),
            )

        # Validate the new password does not match the old password
        if auth_handler.verify_password(data.new_password, current_user.password):
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail="You can't use your old password"
            )

        current_user.password = auth_handler.get_password_hash(data.new_password)
        await self.user_repository.save(current_user)

        return PasswordChangeOutput(message="The password was successfully reset")

    async def export_data_xlsx(self, current_user_id: int):
        await self._validate_user_permissions(self.user_repository, current_user_id)
        return await self.user_repository.export_data_xlsx()

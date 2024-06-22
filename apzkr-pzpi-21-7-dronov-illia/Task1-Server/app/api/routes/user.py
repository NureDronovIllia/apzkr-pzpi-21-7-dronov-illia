from fastapi import APIRouter, Depends

from app.api.dependencies.services import get_user_service
from app.api.dependencies.user import get_current_user
from app.models.db.user import User
from app.models.schemas.users import (
    PasswordChangeInput,
    PasswordChangeOutput,
    UserData,
    UserRegister,
    UserUpdate,
)
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserData])
async def get_users(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> list[UserData]:
    return await user_service.get_users(current_user)


@router.get("/profile/", response_model=UserData)
async def get_profile(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> list[UserData]:
    return await user_service.get_profile(current_user)


@router.post("/register_user/", response_model=UserData, status_code=201)
async def register_user(
    user_data: UserRegister,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserData:
    return await user_service.register_user(user_data, current_user)


@router.patch("/{user_id}/update/", response_model=UserData)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserData:
    return await user_service.update_user(user_id, user_data, current_user)


@router.delete("/{user_id}/delete/", response_model=None, status_code=204)
async def update_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserData:
    return await user_service.delete_user(user_id, current_user)


@router.patch("/change-password/", response_model=PasswordChangeOutput)
async def change_password(
    data: PasswordChangeInput,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> None:
    return await user_service.change_password(current_user, data)

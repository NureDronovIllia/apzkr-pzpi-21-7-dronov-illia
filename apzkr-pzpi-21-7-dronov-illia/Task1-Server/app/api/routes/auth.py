from fastapi import APIRouter, Depends

from app.api.dependencies.services import get_user_service
from app.models.schemas.users import UserLoginInput, UserLoginOutput
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login/", response_model=UserLoginOutput, responses=None)
async def login(
    user_data: UserLoginInput, user_service: UserService = Depends(get_user_service)
) -> UserLoginOutput:
    """
    ### Authenticate and retrieve a JWT token
    """
    return await user_service.authenticate_user(user_data)

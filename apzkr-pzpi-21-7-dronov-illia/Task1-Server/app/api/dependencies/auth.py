from typing import Any, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.dependencies.repository import get_repository
from app.repository.user import UserRepository
from app.securities.authorization.auth_handler import auth_handler


async def auth_wrapper(
    auth: HTTPAuthorizationCredentials = Security(HTTPBearer(auto_error=False)),
) -> Optional[dict[str, Any]]:
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    user_data = await auth_handler.decode_token(auth.credentials)
    return user_data

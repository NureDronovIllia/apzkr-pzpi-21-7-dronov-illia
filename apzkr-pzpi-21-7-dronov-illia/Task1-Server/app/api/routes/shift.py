from fastapi import APIRouter, Depends

from app.api.dependencies.services import get_shift_service
from app.api.dependencies.user import get_current_user
from app.models.db.user import User
from app.models.schemas.shift import ShiftBase, ShiftData
from app.services.shift import ShiftService

router = APIRouter(prefix="/shifts", tags=["Shifts"])


@router.get("/", response_model=list[ShiftData])
async def get_shifts(
    current_user: User = Depends(get_current_user),
    shift_service: ShiftService = Depends(get_shift_service),
) -> list[ShiftData]:
    return await shift_service.get_shifts(current_user)


@router.post("/start/", response_model=ShiftData, status_code=201)
async def start_shift(
    data: ShiftBase,
    current_user: User = Depends(get_current_user),
    shift_service: ShiftService = Depends(get_shift_service),
) -> None:
    return await shift_service.start_shift(data, current_user)


@router.post("/{shift_id}/end/", response_model=ShiftData, status_code=201)
async def end_shift(
    shift_id: int,
    current_user: User = Depends(get_current_user),
    shift_service: ShiftService = Depends(get_shift_service),
) -> ShiftData:
    return await shift_service.end_shift(shift_id, current_user)

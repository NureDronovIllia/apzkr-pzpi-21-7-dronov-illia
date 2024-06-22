import json

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.api.dependencies.services import get_user_service
from app.api.dependencies.user import get_current_user_id
from app.services.user import UserService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/export-data/xlsx/", response_model=None)
async def export_data_xlsx(
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    file_path = await user_service.export_data_xlsx(current_user_id)
    return FileResponse(
        path=file_path, filename="export.xlsx", media_type="multipart/form-data"
    )

@router.post("/send-critical-messages/", response_model=None)
async def send_message(
    data: dict,
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    with open("./messages.json", "r", encoding="utf-8") as file:
        current_data: list = json.loads(file.read())
        current_data.append(data)

    with open("./messages.json", "w", encoding="utf-8") as file:
        file.write(json.dumps((current_data)))


@router.get("/get-critical-messages/", response_model=None)
async def send_message(
    current_user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    with open("./messages.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())

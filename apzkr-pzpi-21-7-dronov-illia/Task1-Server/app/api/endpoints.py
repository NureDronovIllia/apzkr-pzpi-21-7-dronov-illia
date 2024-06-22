from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.fuel import router as fuel_router
from app.api.routes.shift import router as shift_router
from app.api.routes.user import router as user_router
from app.api.routes.vehicle import router as vehicle_router

router = APIRouter()

router.include_router(router=auth_router)
router.include_router(router=user_router)
router.include_router(router=admin_router)
router.include_router(router=vehicle_router)
router.include_router(router=shift_router)
router.include_router(router=fuel_router)

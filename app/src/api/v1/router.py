from fastapi import APIRouter

from src.api.v1.endpoints.auth import router as auth_router
from src.api.v1.endpoints.device import router as device_router
from src.api.v1.endpoints.user import router as user_router

router = APIRouter()

router.include_router(
    router=auth_router,
    prefix='/auth',
    tags=['auth'],
)

router.include_router(
    router=device_router,
    prefix='/devices',
    tags=['devices'],
)

router.include_router(
    router=user_router,
    prefix='/users',
    tags=['users'],
)

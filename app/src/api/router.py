from fastapi import APIRouter

from src.api.v1.router import router as api_v1_router

router = APIRouter()

router.include_router(
    router=api_v1_router,
    prefix='/v1',
)

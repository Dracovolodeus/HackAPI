from fastapi import APIRouter
from .create import router as create_router

router = APIRouter()

router.include_router(create_router)

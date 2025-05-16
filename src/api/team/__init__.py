from fastapi import APIRouter

from core.config import settings
from .create import router as create_router

router = APIRouter(prefix=settings.api.team, tags=["Teams"])

router.include_router(create_router)

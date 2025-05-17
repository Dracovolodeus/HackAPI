from fastapi import APIRouter

from core.config import settings

from .hackathon import router as hackathon_router
from .image import router as image_router
from .team import router as team_router
from .user import router as user_router

router = APIRouter(prefix=settings.api.prefix)

router.include_router(user_router)
router.include_router(hackathon_router)
router.include_router(team_router)
router.include_router(image_router)

from fastapi import APIRouter

from core.config import settings

from .get import router as get_router
from .upload import router as upload_router

router = APIRouter(prefix=settings.api.image, tags=["Images"])
router.include_router(upload_router)
router.include_router(get_router)

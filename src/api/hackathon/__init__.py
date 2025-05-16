from fastapi import APIRouter
from core.config import settings
from .create import router as create_router
from .get import router as get_router
from .add_admin import router as add_admin_router
from .remove_admin import router as remove_admin_router
from .add_jury import router as add_jury_router
from .remove_jury import router as remove_jury_router

router = APIRouter(prefix=settings.api.hackathon, tags=["Hackathons"])

router.include_router(create_router)
router.include_router(get_router)
router.include_router(add_admin_router)
router.include_router(remove_admin_router)
router.include_router(add_jury_router)
router.include_router(remove_jury_router)

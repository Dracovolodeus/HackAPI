from fastapi import APIRouter

from .login import router as login_router
from .resp_pers import router as resp_pers_router
from .root import router as root_router
from .user import router as user_router

router = APIRouter(tags=["Any Users"])

router.include_router(login_router)
router.include_router(user_router)
router.include_router(resp_pers_router)
router.include_router(root_router)

from fastapi import APIRouter

from .create import router as create_router
from .get import router as get_router
from .login import router as login_router

router = APIRouter(prefix="/user", tags=["Users"])

# Include login router
router.include_router(login_router)

# Include create router
router.include_router(create_router)

# Include get router
router.include_router(get_router)

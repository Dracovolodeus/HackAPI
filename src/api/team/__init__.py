from fastapi import APIRouter

from core.config import settings

from .check_want_users import router as check_want_users_router
from .create import router as create_router
from .invite import router as invite_router
from .set_is_activ import router as set_is_activ_router
from .uninvite import router as uninvite_router
from .add_to_want_the_user import router as add_to_want_the_user_router
from .get_all_searchers import router as get_all_searchers_router

router = APIRouter(prefix=settings.api.team, tags=["Teams"])

router.include_router(create_router)
router.include_router(invite_router)
router.include_router(uninvite_router)
router.include_router(check_want_users_router)
router.include_router(set_is_activ_router)
router.include_router(add_to_want_the_user_router)
router.include_router(get_all_searchers_router)

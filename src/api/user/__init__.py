from fastapi import APIRouter

from .check_want_teams import router as check_want_teams_router
from .create import router as create_router
from .get import router as get_router
from .login import router as login_router
from .add_to_want_the_team import router as add_to_want_the_team_router
from .update_description import router as update_description_router
from .set_is_search_team import router as set_is_search_team_router
from .get_all_searches import router as get_all_searches_router

router = APIRouter(prefix="/user", tags=["Users"])

router.include_router(login_router)
router.include_router(create_router)
router.include_router(get_router)
router.include_router(check_want_teams_router)
router.include_router(add_to_want_the_team_router)
router.include_router(update_description_router)
router.include_router(set_is_search_team_router)
router.include_router(get_all_searches_router)

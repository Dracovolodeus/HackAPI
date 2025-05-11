from fastapi import APIRouter

from core.config import settings

from .author import router as author_router
from .book import router as book_router
from .book_tag import router as book_tag_router
from .order import router as order_router
from .role import router as role_router
from .tag import router as tag_router
from .user import router as user_router

router = APIRouter(
    prefix=settings.api.prefix,
)

# Include author router
router.include_router(
    author_router,
    prefix=settings.api.author,
)

# Include book router
router.include_router(
    book_router,
    prefix=settings.api.book,
)

# Include book_tag router
router.include_router(
    book_tag_router,
    prefix=settings.api.book_tag,
)

# Include order router
router.include_router(
    order_router,
    prefix=settings.api.order,
)

# Include roles router
router.include_router(
    role_router,
    prefix=settings.api.role,
)

# Include tag router
router.include_router(
    tag_router,
    prefix=settings.api.tag,
)

# Include users router
router.include_router(
    user_router,
    prefix=settings.api.user,
)

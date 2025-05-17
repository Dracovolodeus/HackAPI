from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.user.set_is_search_team import set_is_search_team as crud_set_is_search_team
from database import User, db_helper

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.set_is_search}"
)
async def set_is_search_team(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    condition: bool
):
    await crud_set_is_search_team(session=session, user=caller_user, condition=condition)

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.user.get_many_users import get_many_users as crud_get_many_users
from database import User, db_helper

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.check_users_want_join_to_team}",
    status_code=status.HTTP_200_OK,
    response_model=tuple,
)
async def check_users_want_join_to_team(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud_get_many_users(
        session=session, users_ids=tuple(caller_user.want_join_to_team_ids)
    )

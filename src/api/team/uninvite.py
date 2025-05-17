from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.team.uninvite_user import \
    remove_user_from_team as crud_remove_user_from_team
from database import User, db_helper
from exceptions.any import NotFoundError

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.uninvite}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "User not in the team error"},
        200: {"description": "OK"},
    },
)
async def uninvite_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
    team_id: int,
):
    try:
        await crud_remove_user_from_team(
            session=session, user_id=user_id, team_id=team_id
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not in the team error"
        )


@router.post(
    f"{settings.api.uninvite}{settings.api.self}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "User not in the team error"},
        200: {"description": "OK"},
    },
)
async def self_uninvite_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    team_id: int,
):
    try:
        await crud_remove_user_from_team(
            session=session, user_id=caller_user["id"], team_id=team_id
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not in the team error"
        )

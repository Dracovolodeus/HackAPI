from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as get_crud
from crud.team.add_want_user import add_want_team_for_user
from database import Team, User, db_helper
from exceptions.any import NotFoundError
from exceptions.invite import DuplicateError

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(f"{settings.api.add}{settings.api.want_the_team}", status_code=status.HTTP_200_OK)
async def add_to_want_the_team(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    team_id: int
):
    try:
        await add_want_team_for_user(session=session, team_id=team_id, user_id=caller_user.id)
    except DuplicateError:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="already added"
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found error"
        )
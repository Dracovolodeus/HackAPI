from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as get_crud
from crud.user.get_many_users import get_many_users as crud_get_many_users
from database import Team, User, db_helper
from exceptions.any import NotFoundError

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.check_users_want_join_to_team}", status_code=status.HTTP_200_OK
)
async def check_users_want_join_to_team(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    team_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    try:
        team: Team = await get_crud(session=session, db_model=Team, object_id=team_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found error"
        )
    if team.leader_id != caller_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not a leader error"
        )
    return await crud_get_many_users(team.want_join_to_team_ids)

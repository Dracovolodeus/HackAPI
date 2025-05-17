from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as get_crud
from crud.team.set_is_active import set_is_active as crud_set_is_active
from database import Team, User, db_helper
from exceptions.any import NotFoundError
from exceptions.invite import DuplicateError

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(f"{settings.api.set_is_activ}", status_code=status.HTTP_200_OK)
async def set_is_activ(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    team_id: int,
    condition: bool,
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
    try:
        await crud_set_is_active(session=session, team_id=team_id, condition=condition)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found error"
        )
    except DuplicateError:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="Not changed"
        )

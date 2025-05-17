from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as crud_get
from crud import get_user_by_email
from crud.hackathon import remove_team as crud_remove_team
from database import Hackathon, User, db_helper
from exceptions.any import NotFoundError

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.team}{settings.api.remove}",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "OK"}, 404: {"description": "Not found error"}},
)
async def remove_team(
    team_email: str,
    hackathon_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    current_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    try:
        team_member = await get_user_by_email(session=session, email=team_email)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found error"
        )
    try:
        hackathon: Hackathon = await crud_get(
            object_id=hackathon_id, db_model=Hackathon, session=session
        )
        if current_user.id != hackathon.creator_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
            )

        await crud_remove_team.remove_team(
            session=session, hackathon=hackathon, team_member=team_member
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found hackathon error"
        )

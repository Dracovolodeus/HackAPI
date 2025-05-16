from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..validation import get_current_user_from_access_token
from core.config import settings
from crud import create as crud_create
from database import Team, db_helper, User
from schemas.team import TeamCreate, TeamCreateForAPI, TeamRead

router = APIRouter()


@router.post(
    f"{settings.api.create}",
    status_code=status.HTTP_201_CREATED,
    response_model=TeamRead,
    responses={
        201: {"description": "Team created"}
    }
)
async def create_team(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        team_create: TeamCreateForAPI,
        caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    team = await crud_create(
        session=session,
        create=TeamCreate(**team_create, leader_id=caller_user.id),
        db_model=Team
    )
    return team

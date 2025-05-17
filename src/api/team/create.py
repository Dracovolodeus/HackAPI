from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_url_token
from core.config import settings
from crud import create as crud_create
from crud import get as get_crud
from crud.hackathon.add_team import add_team as crud_add_team
from crud.team.invite_user import add_user_to_team as crud_add_user_to_int
from database import Hackathon, Team, User, db_helper
from exceptions.any import NotFoundError
from exceptions.invite import DuplicateError
from schemas.team import TeamAndURL, TeamCreate, TeamCreateForAPI, TeamRead

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.create}",
    status_code=status.HTTP_201_CREATED,
    response_model=TeamAndURL,
    responses={201: {"description": "Team created"}, 401: {"description": "Bad token"}},
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
        create=TeamCreate(**team_create.model_dump(), leader_id=caller_user.id),
        db_model=Team,
    )
    try:
        await crud_add_user_to_int(
            session=session, user_id=team.leader_id, team_id=team.id
        )
    except DuplicateError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user is already a team member error",
        )
    try:
        await crud_add_team(
            session=session,
            hackathon=await get_crud(
                session=session, object_id=team.hackathon_id, db_model=Hackathon
            ),
            team=team,
        )
    except NotFoundError:
        ...
    return TeamAndURL(
        read=TeamRead(
            name=team.name,
            idea=team.idea,
            idea_detail=team.idea_detail,
            leader_id=team.leader_id,
            hackathon_id=team.hackathon_id,
        ),
        url=(
            settings.run.url
            + settings.api.invite
            + settings.api.login
            + "/"
            + create_url_token(team_id=team.id)
        ),
    )

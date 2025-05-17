from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_url_token
from auth.utils import decode_jwt
from core.config import settings
from crud import get as crud_get
from crud.team.invite_user import add_user_to_team as crud_add_user_to_int
from database import Team, User, db_helper
from exceptions.any import NotFoundError
from exceptions.invite import DuplicateError
from schemas.invite_url import InviteURLCreate, InviteURLRead

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.invite}{settings.api.create}",
    status_code=status.HTTP_200_OK,
    response_model=InviteURLRead,
    responses={
        404: {"description": "Team not found error"},
        403: {"description": "This is not your team error"},
    },
)
async def create_invite_url(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    url_create: InviteURLCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    try:
        team: Team = await crud_get(
            session=session, db_model=Team, object_id=url_create.team_id
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found error"
        )
    if team.leader_id != caller_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This is not your team error"
        )
    return InviteURLRead(
        url=(
            settings.run.url
            + settings.api.prefix
            + settings.api.team
            + settings.api.invite
            + settings.api.login
            + "/"
            + create_url_token(team_id=url_create.team_id)
        )
    )


@router.get(
    f"{settings.api.invite}{settings.api.login}/{{url}}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "OK"},
        401: {"description": "Bad or invalid token error"},
    },
)
async def login_invite_url(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    url: str,
):
    try:
        jwt_payload = decode_jwt(token=url)
        if jwt_payload["type"] != settings.auth_jwt.url_token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token type error"
            )
        try:
            await crud_add_user_to_int(
                session=session, user_id=caller_user.id, team_id=jwt_payload["id"]
            )
        except DuplicateError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user is already a team member error",
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token error"
        )

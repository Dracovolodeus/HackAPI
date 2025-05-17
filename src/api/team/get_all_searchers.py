from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as get_crud
from crud.team.get_all_searchers import get_all_searchers as crud_get_all_searchers
from database import Team, User, db_helper
from exceptions.any import NotFoundError
from exceptions.invite import DuplicateError
from schemas.team import TeamRead

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.get(
    f"{settings.api.get_all_searches}",
    status_code=status.HTTP_200_OK,
    response_model=list
)
async def get_all_searchers(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return [TeamRead(
        name=i.name, idea=i.idea, idea_detail=i.idea_detail, leader_id=i.leader_id, hackathon_id=i.hackathon_id
    ) for i in (await crud_get_all_searchers(session))]


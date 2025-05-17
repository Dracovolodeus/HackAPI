from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import create as crud_create
from database import Hackathon, User, db_helper
from schemas.hackathon import (HackathonCreate, HackathonCreateForAPI,
                               HackathonRead)

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.create}",
    status_code=status.HTTP_201_CREATED,
    response_model=HackathonRead,
    responses={201: {"description": "Hackathon created"}},
)
async def create_hackathon(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    hackathon_create: HackathonCreateForAPI,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    hackathon = await crud_create(
        session=session,
        db_model=Hackathon,
        create=HackathonCreate(
            **hackathon_create.model_dump(),
            creator_user_id=caller_user.id,
        ),
    )
    return hackathon

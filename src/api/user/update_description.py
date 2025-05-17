from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.user.update_description import update_description as crud_update_description
from database import User, db_helper

from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.post(
    f"{settings.api.description}{settings.api.update}",
    status_code=status.HTTP_200_OK,
)
async def update_description(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    new_description: str
):
    await crud_update_description(session=session, user=caller_user, new_desc=new_description)

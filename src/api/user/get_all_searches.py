from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.user.get_all_searchers import get_all_searchers as crud_get_all_searchers
from database import db_helper
from schemas.user import UserPartRead

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
    return [UserPartRead(
        id=i.id, first_name=i.first_name, last_name=i.last_name, second_name=i.second_name,
        description=i.description, email=i.email
    ) for i in (await crud_get_all_searchers(session=session))]

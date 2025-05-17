from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get_all as crud_get_all
from database import Hackathon, db_helper

router = APIRouter()


@router.get(
    f"{settings.api.get_all}",
    status_code=status.HTTP_200_OK,
)
async def get_all_hackathons(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud_get_all(session=session, db_model=Hackathon)

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from crud import get as crud_get
from database import Hackathon, db_helper
from schemas.hackathon import HackathonRead
from exceptions.any import NotFoundError

router = APIRouter()


@router.get(
    f"{settings.api.get}",
    status_code=status.HTTP_200_OK,
    response_model=HackathonRead,
    responses={
        200: {"description": "OK"},
        401: {"description": "Invalid token error"},
        404: {"description": "Hackathon not found error"}
    },
)
async def get_hackathon(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    hackathon_id: int,
):
    try:
        hackathon = await crud_get(session=session, db_model=Hackathon, object_id=hackathon_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hackathon not found error"
        )
    return hackathon

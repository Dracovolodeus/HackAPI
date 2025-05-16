from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from database import db_helper, Hackathon, User
from crud import get_user_by_email
from crud import get as crud_get
from crud.hackathon import add_jury as crud_add_jury
from exceptions.any import NotFoundError
from ..validation import get_current_user_from_access_token

router = APIRouter()

@router.post(
    f"{settings.api.jury}{settings.api.add}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "OK"},
        404: {"description": "Not found error"}
    }
)
async def add_jury(
        jury_email: str,
        hackathon_id: int,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        current_user: Annotated[User, Depends(get_current_user_from_access_token)]
):
    try:
        jury = await get_user_by_email(session=session, email=jury_email)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Jury not found error"
        )
    try:

        hackathon: Hackathon = await crud_get(object_id=hackathon_id, db_model=Hackathon, session=session)
        if current_user.id != hackathon.creator_user_id:
            HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
            )

        await crud_add_jury.add_jury(
            session=session, hackathon=hackathon, jury=jury
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found hackathon error"
        )

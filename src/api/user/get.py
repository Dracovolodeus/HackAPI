from typing import Annotated

from fastapi import APIRouter, Depends, status

from core.config import settings
from database import User
from ..validation import get_current_user_from_access_token

router = APIRouter()


@router.get(
    f"{settings.api.user}{settings.api.get}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "OK"},
        401: {"description": "Invalid token error"},
    },
)
async def get_user(
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    return caller_user

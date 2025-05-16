from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as crud_get
from database import User, db_helper
from schemas.user import UserCreate, UserRead

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

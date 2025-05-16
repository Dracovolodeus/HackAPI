from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import create as crud_create
from database import User, db_helper
from schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post(
    f"{settings.api.create}",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    responses={201: {"description": "User created"}},
)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_create: UserCreate,
):
    try:
        user = await crud_create(create=user_create, db_model=User, session=session)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email is busy")
    return user

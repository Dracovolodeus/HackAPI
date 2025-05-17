from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import get as get_crud
from crud.user.get_many_users import get_many_users as crud_get_many_users
from database import Hackathon, Team, User, db_helper
from exceptions.any import NotFoundError

from ..validation import get_current_user_from_access_token

router = APIRouter()


router.post()
async def accept_want_user():
    ...
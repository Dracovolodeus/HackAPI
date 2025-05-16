from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..validation import get_current_user_from_access_token
from core.config import settings
from crud import create as crud_create
from database import Team, db_helper, User
from schemas.team import TeamCreate, TeamCreateForAPI, TeamRead

router = APIRouter()

@router.post(
    f"{settings.api.invite}"
)
async def create_invite_url():
    ...

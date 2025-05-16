import time
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_access_token
from core.config import settings
from crud.login import login as crud_login
from database import db_helper
from schemas.token import AccessToken
from schemas.user import UserLogin
from api.validation import get_current_token_payload

router = APIRouter()


@router.post(
    f"{settings.api.login}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful authentication"},
        400: {"description": "No data received"},
        401: {"description": "Unsuccessful authentication"},
    },
)
async def login(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_login: UserLogin,
):
    return await crud_login(
        session=session,
        email=user_login.email,
        password=user_login.password,
    )


@router.post(
    f"{settings.api.update_access_token}",
    response_model=AccessToken,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful update"},
        401: {"description": "Bad token error"},
    },
)
async def update_access_token(
    token_payload: Annotated[dict, Depends(get_current_token_payload)],
):
    exp = token_payload.get("exp")
    if (token_type := token_payload.get(settings.auth_jwt.token_type_field)) is None:
        print(f"\n1\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token error"
        )
    elif token_type != settings.auth_jwt.refresh_token_type:
        print(f"\n2\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token type error"
        )
    elif exp is not None and exp <= time.time():
        print(f"\n3\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired error"
        )
    return AccessToken(token=create_access_token(token_payload["id"]))

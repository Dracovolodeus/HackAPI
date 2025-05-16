import time
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import decode_jwt
from core.config import settings
from crud import get as crud_get
from database import User, db_helper
from exceptions.any import NotFoundError

http_bearer = HTTPBearer()


async def get_any_user(session: AsyncSession, any_user_id: int) -> User:
    return await crud_get(session=session, object_id=any_user_id, db_model=User)


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    try:
        payload = decode_jwt(token=credentials.credentials)
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token error"
        )


async def get_current_user_from_access_token(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    token_payload = await get_current_token_payload(credentials)
    exp = token_payload.get("exp")
    if (token_type := token_payload.get(settings.auth_jwt.token_type_field)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token error"
        )
    elif token_type != settings.auth_jwt.access_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token type error"
        )
    elif exp is not None and exp <= time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired error"
        )
    try:
        return await crud_get(
            session=session, db_model=User, object_id=token_payload["id"]
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bad token error"
        )

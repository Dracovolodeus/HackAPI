from datetime import datetime, timedelta
from random import randint
from typing import Optional

from core.config import settings

from .utils import encode_jwt


def create_jwt(
    token_type: str,
    token_data: dict,
) -> str:
    """ """
    payload = {settings.auth_jwt.token_type_field: token_type}
    payload.update(token_data)

    return encode_jwt(payload=payload)


def create_access_token(
    user_id: int,
    exp: Optional[int] = None,
) -> str:
    now = datetime.now()
    dict_exp_delta = settings.auth_jwt.access_token_expire_seconds
    if exp is not None:
        dict_exp_delta = exp
    payload = {
        "sub": str(user_id),
        "jti": f"{randint(5, 9)}{now.year}{user_id}{now.microsecond}{now.minute}{now.day}{now.second}{now.month}{randint(0, 4)}",
        "id": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=dict_exp_delta)).timestamp()),
    }
    return create_jwt(
        token_type=settings.auth_jwt.access_token_type, token_data=payload
    )


def create_refresh_token(
    user_id: int,
    exp: Optional[int] = None,
) -> str:
    now = datetime.now()
    dict_exp_delta = settings.auth_jwt.access_token_expire_seconds
    if exp is not None:
        dict_exp_delta = exp
    payload = {
        "sub": str(user_id),
        "jti": f"{randint(0, 4)}{now.year}{user_id}{now.microsecond}{now.minute}{now.day}{now.second}{now.month}{randint(5, 9)}",
        "id": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=dict_exp_delta)).timestamp()),
    }
    return create_jwt(
        token_type=settings.auth_jwt.refresh_token_type, token_data=payload
    )


def create_url_token(
    team_id: int,
    exp: int = settings.auth_jwt.invite_url_expire_seconds,
):
    now = datetime.now()
    payload = {
        "sub": str(team_id),
        "id": team_id,
        "jti": f"{randint(10, 99)}{now.year}{team_id}{now.microsecond}{now.minute}{now.day}{now.second}{now.month}{randint(0, 9)}",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=exp)).timestamp()),
    }
    return create_jwt(token_type=settings.auth_jwt.url_token_type, token_data=payload)

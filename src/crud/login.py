from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_refresh_token
from auth.utils import validate_password
from database.tables.user import User


async def login(
    session: AsyncSession,
    password: Optional[str],
    email: Optional[str],
    telegram_id: Optional[int],
) -> str:
    query = select(User)

    if email is not None and password is not None:
        result = (
            (await session.execute(query.where(User.email == email))).scalars().first()
        )
        if result is None or not validate_password(
            password=password, hashed_password=result.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        elif telegram_id is not None and result.telegram_id != telegram_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email and password or telegram_id",
            )
    elif telegram_id:
        result = (
            (await session.execute(query.where(User.telegram_id == telegram_id)))
            .scalars()
            .first()
        )
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid telegram_id",
            )
        elif (
            email is not None
            and password is not None
            and result.email != email
            and not validate_password(
                password=password, hashed_password=result.password
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email and password or telegram_id",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data received"
        )

    result.refresh_token
    new_refresh_token = create_refresh_token(result.id)
    result.refresh_token = new_refresh_token
    await session.commit()
    return new_refresh_token

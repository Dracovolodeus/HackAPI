from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.user import User
from exceptions.any import NotFoundError


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    result = (
        (await session.execute(select(User).where(User.email == email)))
        .scalars()
        .first()
    )
    if result is None:
        raise NotFoundError
    return result

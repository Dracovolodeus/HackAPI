from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import User


async def get_many_users(session: AsyncSession, users_ids: tuple) -> tuple:
    result = await session.execute(select(User).where(User.id.in_(users_ids)))
    return tuple(result.scalars().all())

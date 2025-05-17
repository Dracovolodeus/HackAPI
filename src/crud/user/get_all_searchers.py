from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import User


async def get_all_searchers(
    session: AsyncSession,
):
    result = await session.execute(select(User).where(User.is_search == True))
    return result.scalars().all()

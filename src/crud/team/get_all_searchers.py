from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import Team


async def get_all_searchers(
    session: AsyncSession,
):
    result = await session.execute(select(Team).where(Team.need_roles != []))
    return result.scalars().all() or []

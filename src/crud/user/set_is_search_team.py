from sqlalchemy.ext.asyncio import AsyncSession

from database import User


async def set_is_search_team(
    session: AsyncSession,
    user: User,
    condition: bool
):
    user.is_search = condition
    session.add(user)
    await session.commit()
    await session.refresh(user)

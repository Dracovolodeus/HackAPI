from sqlalchemy.ext.asyncio import AsyncSession

from database import User


async def update_description(
        session: AsyncSession,
        user: User,
        new_desc: str
):
    if new_desc.lstrip().rstrip() == '':
        new_desc = None
    user.description = new_desc
    session.add(user)
    await session.commit()
    await session.refresh(user)

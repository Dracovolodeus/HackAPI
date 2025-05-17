from sqlalchemy.ext.asyncio import AsyncSession

from database import Hackathon, User
from exceptions.any import NotFoundError


async def remove_admin(session: AsyncSession, hackathon: Hackathon, admin: User):
    if admin.id not in hackathon.admins_ids:
        raise NotFoundError
    hackathon.admins_ids.remove(admin.id)
    session.add(hackathon)
    await session.commit()

from sqlalchemy.ext.asyncio import AsyncSession

from database import Hackathon, User
from exceptions.invite import DuplicateError


async def add_admin(session: AsyncSession, hackathon: Hackathon, admin: User):
    if admin.id in hackathon.admins_ids:
        raise DuplicateError
    hackathon.admins_ids.append(admin.id)
    session.add(hackathon)
    await session.commit()

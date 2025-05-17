from sqlalchemy.ext.asyncio import AsyncSession

from database import Hackathon, User
from exceptions.any import NotFoundError


async def remove_jury(session: AsyncSession, hackathon: Hackathon, jury: User):
    if jury.id not in hackathon.jury_ids:
        raise NotFoundError
    hackathon.jury_ids.remove(jury.id)
    session.add(hackathon)
    await session.commit()

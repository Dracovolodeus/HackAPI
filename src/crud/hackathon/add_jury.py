from sqlalchemy.ext.asyncio import AsyncSession

from database import Hackathon, User
from exceptions.invite import DuplicateError


async def add_jury(session: AsyncSession, hackathon: Hackathon, jury: User):
    if jury.id in hackathon.jury_ids:
        raise DuplicateError
    hackathon.jury_ids.append(jury.id)
    session.add(hackathon)
    await session.commit()

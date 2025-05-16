from sqlalchemy.ext.asyncio import AsyncSession
from database import User, Hackathon


async def remove_jury(session: AsyncSession, hackathon: Hackathon, jury: User):
    hackathon.jury_ids.remove(jury.id)
    session.add(hackathon)
    await session.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from database import User, Hackathon


async def add_jury(session: AsyncSession, hackathon: Hackathon, jury: User):
    hackathon.jury_ids.append(jury.id)
    session.add(hackathon)
    await session.commit()

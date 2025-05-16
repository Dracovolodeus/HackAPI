from sqlalchemy.ext.asyncio import AsyncSession
from database import User, Hackathon


async def add_admin(session: AsyncSession, hackathon: Hackathon, admin: User):
    hackathon.admins_ids.append(admin.id)
    session.add(hackathon)
    await session.commit()

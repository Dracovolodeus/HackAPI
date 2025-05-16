from sqlalchemy.ext.asyncio import AsyncSession
from database import User, Hackathon


async def remove_admin(session: AsyncSession, hackathon: Hackathon, admin: User):
    hackathon.admins_ids.remove(admin.id)
    session.add(hackathon)
    await session.commit()

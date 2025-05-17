from sqlalchemy.ext.asyncio import AsyncSession

from database import Hackathon, Team
from exceptions.any import NotFoundError


async def remove_team(session: AsyncSession, hackathon: Hackathon, team: Team):
    if team.id not in hackathon.teams_ids:
        raise NotFoundError
    hackathon.teams_ids.remove(team.id)
    session.add(hackathon)
    await session.commit()

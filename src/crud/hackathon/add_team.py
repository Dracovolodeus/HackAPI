from sqlalchemy.ext.asyncio import AsyncSession

from database import Hackathon, Team
from exceptions.invite import DuplicateError


async def add_team(session: AsyncSession, hackathon: Hackathon, team: Team):
    if team.id in hackathon.teams_ids:
        raise DuplicateError
    hackathon.teams_ids.append(team.id)
    session.add(hackathon)
    await session.commit()

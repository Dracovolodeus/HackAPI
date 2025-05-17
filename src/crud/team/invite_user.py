from sqlalchemy.ext.asyncio import AsyncSession

from database import Team
from exceptions.invite import DuplicateError

from ..get import get as crud_get


async def add_user_to_team(session: AsyncSession, user_id: int, team_id: int):
    team: Team = await crud_get(session=session, db_model=Team, object_id=team_id)
    if user_id in team.teammates_ids:
        raise DuplicateError
    team.teammates_ids.append(user_id)
    session.add(team)
    await session.commit()

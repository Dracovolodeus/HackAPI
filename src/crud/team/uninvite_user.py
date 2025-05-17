from sqlalchemy.ext.asyncio import AsyncSession

from database import Team
from exceptions.any import NotFoundError

from ..get import get as crud_get


async def remove_user_from_team(session: AsyncSession, user_id: int, team_id: int):
    team: Team = await crud_get(session=session, db_model=Team, object_id=team_id)
    if user_id not in team.teammates_ids:
        raise NotFoundError
    team.teammates_ids.remove(user_id)
    session.add(team)
    await session.commit()

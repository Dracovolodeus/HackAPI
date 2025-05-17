from sqlalchemy.ext.asyncio import AsyncSession

from database import Team
from exceptions.invite import DuplicateError

from ..get import get as crud_get


async def set_is_active(session: AsyncSession, team_id: int, condition: bool):
    team: Team = await crud_get(session=session, db_model=Team, object_id=team_id)
    if team.is_activ == condition:
        raise DuplicateError
    team.is_activ = condition
    session.add(team)
    await session.commit()

from sqlalchemy.ext.asyncio import AsyncSession

from database import User, Team
from exceptions.invite import DuplicateError

from ..get import get as get_crud


async def add_want_team_for_user(
        session: AsyncSession, team_id: int, user_id: int
):
    team: Team = await get_crud(session=session, db_model=Team, object_id=team_id)
    if user_id in team.want_join_to_team_ids:
        raise DuplicateError
    team.want_join_to_team_ids.append(user_id)
    session.add(team)
    await session.commit()
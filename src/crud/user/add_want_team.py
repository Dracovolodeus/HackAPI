from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from exceptions.invite import DuplicateError

from ..get import get as get_crud


async def add_want_user_for_team(session: AsyncSession, team_id: int, user_id: int):
    user: User = await get_crud(session=session, db_model=User, object_id=user_id)
    if team_id in user.want_join_to_team_ids:
        raise DuplicateError
    user.want_join_to_team_ids.append(team_id)
    session.add(user)
    await session.commit()

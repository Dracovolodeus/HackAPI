from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

DbModel = TypeVar("DbModel", bound=DeclarativeBase)


async def get_all(db_model: DbModel, session: AsyncSession):
    result = await session.execute(select(db_model))
    return result.scalars().all()

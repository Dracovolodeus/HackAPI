from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from exceptions.any import NotFoundError

DbModel = TypeVar("DbModel", bound=DeclarativeBase)


async def get(object_id: int, db_model: DbModel, session: AsyncSession):

    # Create an instance of database class
    object = await session.get(db_model, object_id)
    if object is None:
        raise NotFoundError

    return object

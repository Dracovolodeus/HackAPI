from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

PydanticCreate = TypeVar("PydanticCreate", bound=BaseModel)
DbModel = TypeVar("DbModel", bound=DeclarativeBase)


async def create(create: PydanticCreate, db_model: DbModel, session: AsyncSession):

    # Create an instance of database class
    object = db_model(**create.model_dump())

    session.add(object)
    await session.commit()

    return object

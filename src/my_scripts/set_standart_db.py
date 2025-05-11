
import asyncio
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

DATABASE_URL = "postgresql+asyncpg://root:ytrewq@localhost:5432/library"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def main():
    ...

if __name__ == "__main__":
    asyncio.run(main())


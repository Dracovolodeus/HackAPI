from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import Image


async def upload(session: AsyncSession, image: UploadFile):
    data = await image.read()
    db_image = Image(data=data)
    session.add(db_image)
    await session.commit()
    await session.refresh(db_image)
    return db_image

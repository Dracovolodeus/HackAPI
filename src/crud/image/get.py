from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import Image

from ..get import get as crud_get


async def get_image(image_id: int, session: AsyncSession):
    return await crud_get(session=session, db_model=Image, object_id=image_id)

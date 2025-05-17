from typing import Annotated

from fastapi import (APIRouter, Depends, File, HTTPException, Response,
                     UploadFile, status)
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.image.get import get_image as crud_get
from database import Image, db_helper
from exceptions.any import NotFoundError

router = APIRouter()


@router.get(
    f"{settings.api.get}{{image_id}}",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
async def get_image(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    image_id: int,
):
    try:
        image = await crud_get(session=session, image_id=image_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found error"
        )
    return Response(content=bytes(image.data), media_type=image.content_type)

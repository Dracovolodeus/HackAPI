from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.image.upload import upload as crud_upload
from database import Image, db_helper

router = APIRouter()


@router.post(
    f"{settings.api.upload}", status_code=status.HTTP_200_OK, response_model=None
)
async def upload_image(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    file: UploadFile = File(..., max_size=10_000_000),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type"
        )
    img = await crud_upload(session=session, image=file)
    return {"id": img.id}

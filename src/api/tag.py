from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import tag as tags_crud
from database import User, db_helper
from schemas.tag import TagCreate, TagFullUpdate, TagPartUpdate, TagRead

from .validation import get_current_user_from_access_token, verify_token_user_identity

router = APIRouter(tags=["Tags"])


@router.post(
    f"{settings.api.create}",
    response_model=TagRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Tag created"},
        422: {"description": "Validation error"},
        403: {"description": "Not enough rights error"},
    },
)
async def create_tag(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    tag_create: TagCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    tag = await tags_crud.create_tag(
        session=session,
        tag_create=tag_create,
    )
    return tag


@router.get(
    f"{settings.api.get}",
    response_model=TagRead,
    responses={
        404: {"description": "Tag not found"},
        403: {"description": "Not enough rights error"},
    },
)
async def get_tag(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    tag_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await tags_crud.get_tag(session=session, tag_id=tag_id)


@router.patch(
    f"{settings.api.full_update}",
    response_model=TagRead,
    responses={
        404: {"description": "Tag not found"},
        403: {"description": "Not enough rights error"},
        304: {"description": "Tag not modified"},
    },
)
async def full_right_update_tag(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    tag_update: TagFullUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await tags_crud.update_tag(session=session, tag_update=tag_update)


@router.patch(
    f"{settings.api.part_update}",
    response_model=TagRead,
    responses={
        404: {"description": "Tag not found"},
        304: {"description": "Tag not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def part_right_update_tag(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    tag_update: TagPartUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await tags_crud.update_tag(session=session, tag_update=tag_update)


@router.delete(
    f"{settings.api.delete}/{{tag_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Tag not found"},
        204: {"description": "Tag deleted successfully"},
        403: {"description": "Not enough rights error"},
    },
)
async def delete_tag(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    tag_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await tags_crud.delete_tag(session=session, tag_id=tag_id)

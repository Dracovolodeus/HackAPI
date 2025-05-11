from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import book_tag as book_tags_crud
from database import User, db_helper
from schemas.book_tag import (BookTagCreate, BookTagFullUpdate,
                              BookTagPartUpdate, BookTagRead)

from .validation import get_current_user_from_access_token, verify_token_user_identity

router = APIRouter(tags=["Book Tag"])


@router.post(
    f"{settings.api.create}",
    response_model=BookTagRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "BookTag created"},
        422: {"description": "Validation error"},
        403: {"description": "Not enough rights error"},
    },
)
async def create_book_tag(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    book_tag_create: BookTagCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    book_tag = await book_tags_crud.create_book_tag(
        session=session,
        book_tag_create=book_tag_create,
    )
    return book_tag


@router.get(
    f"{settings.api.get}",
    response_model=BookTagRead,
    responses={404: {"description": "BookTag not found"}},
)
async def get_book_tag(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    book_tag_id: int,
):
    return await book_tags_crud.get_book_tag(session=session, book_tag_id=book_tag_id)


@router.patch(
    f"{settings.api.full_update}",
    response_model=BookTagRead,
    responses={
        404: {"description": "BookTag not found"},
        304: {"description": "BookTag not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def full_right_update_book_tag(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    book_tag_update: BookTagFullUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await book_tags_crud.update_book_tag(
        session=session, book_tag_update=book_tag_update
    )


@router.patch(
    f"{settings.api.part_update}",
    response_model=BookTagRead,
    responses={
        404: {"description": "BookTag not found"},
        304: {"description": "BookTag not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def part_right_update_book_tag(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    book_tag_update: BookTagPartUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await book_tags_crud.update_book_tag(
        session=session, book_tag_update=book_tag_update
    )


@router.delete(
    f"{settings.api.delete}/{{book_tag_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "BookTag not found"},
        204: {"description": "BookTag deleted successfully"},
        403: {"description": "Not enough rights error"},
    },
)
async def delete_book_tag(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    book_tag_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await book_tags_crud.delete_book_tag(
        session=session, book_tag_id=book_tag_id
    )

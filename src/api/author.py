from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import author as authors_crud
from database import User, db_helper
from schemas.author import (AuthorCreate, AuthorFullUpdate, AuthorPartUpdate,
                            AuthorRead)

from .validation import get_current_user_from_access_token, verify_token_user_identity

router = APIRouter(tags=["Author"])


@router.post(
    f"{settings.api.create}",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Author created"},
        422: {"description": "Validation error"},
        403: {"description": "Not enough rights error"},
    },
)
async def create_author(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    author_create: AuthorCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    author = await authors_crud.create_author(
        session=session,
        author_create=author_create,
    )
    return author


@router.get(
    f"{settings.api.get}",
    response_model=AuthorRead,
    responses={
        404: {"description": "Author not found"},
        403: {"description": "Not enough rights error"},
    },
)
async def get_author(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    author_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await authors_crud.get_author(session=session, author_id=author_id)


@router.patch(
    f"{settings.api.full_update}",
    response_model=AuthorRead,
    responses={
        404: {"description": "Author not found"},
        304: {"description": "Author not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def full_right_update_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    author_update: AuthorFullUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await authors_crud.update_author(
        session=session, author_update=author_update
    )


@router.patch(
    f"{settings.api.part_update}",
    response_model=AuthorRead,
    responses={
        404: {"description": "Author not found"},
        304: {"description": "Author not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def part_right_update_author(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    author_update: AuthorPartUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await authors_crud.update_author(
        session=session, author_update=author_update
    )


@router.delete(
    f"{settings.api.delete}/{{author_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Author not found"},
        204: {"description": "Author deleted successfully"},
        403: {"description": "Not enough rights error"},
    },
)
async def delete_author(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    author_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await authors_crud.delete_author(session=session, author_id=author_id)

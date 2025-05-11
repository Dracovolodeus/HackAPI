from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import book as books_crud
from database import User, db_helper
from schemas.book import BookCreate, BookFullUpdate, BookPartUpdate, BookRead

from .validation import get_current_user_from_access_token, verify_token_user_identity

router = APIRouter(tags=["Book"])


@router.post(
    f"{settings.api.create}",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Author created"},
        422: {"description": "Validation error"},
        403: {"description": "Not enough rights error"},
    },
)
async def create_book(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    book_create: BookCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    book = await books_crud.create_book(
        session=session,
        book_create=book_create,
    )

    return book


@router.get(
    f"{settings.api.get}",
    response_model=BookRead,
    responses={
        404: {"description": "Book not found"},
        403: {"description": "Not enough rights error"},
    },
)
async def get_book(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    book_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user,
        roles=(settings.role.user, settings.role.resp_pers, settings.role.root),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    book = await books_crud.get_book(session=session, book_id=book_id)
    return book


@router.patch(
    f"{settings.api.full_update}",
    response_model=BookRead,
    responses={
        404: {"description": "Book not found"},
        304: {"description": "Book not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def full_right_update_book(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    book_update: BookFullUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await books_crud.update_book(session=session, book_update=book_update)


@router.patch(
    f"{settings.api.part_update}",
    response_model=BookRead,
    responses={
        404: {"description": "Book not found"},
        304: {"description": "Book not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def part_right_update_book(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    book_update: BookPartUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await books_crud.update_book(session=session, book_update=book_update)


@router.delete(
    f"{settings.api.delete}/{{book_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Book not found"},
        403: {"description": "Not enough rights error"},
        204: {"description": "Book deleted successfully"},
    },
)
async def delete_book(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    book_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await books_crud.delete_book(session=session, book_id=book_id)

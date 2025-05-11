from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import any_user as users_crud
from database import db_helper
from database.tables.user import User
from schemas.any_user import (UserCreate, UserFullUpdate, UserPartUpdate,
                              UserRead, UserSelfUpdate)

from ..validation import (get_current_user_from_access_token, verify_is_i,
                          verify_token_user_identity)

router = APIRouter(tags=["Responsible Person"])


@router.post(
    f"{settings.api.create}{settings.api.resp_pers}",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created"},
        401: {"description": "Invalid token error"},
        403: {"description": "Not enough rights error"},
        404: {"description": "Role not found error"},
        422: {"description": "Validation error"},
    },
)
async def create_resp_pers(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    resp_pers_create: UserCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await users_crud.create_any_user(
        any_user_create=resp_pers_create,
        session=session,
        role_id=settings.role.resp_pers,
    )


@router.get(
    f"{settings.api.get}{settings.api.resp_pers}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User issued"},
        401: {"description": "Invalid token error"},
        403: {"description": "Not enough rights error"},
        404: {"description": "User not found error"},
    },
)
async def get_resp_pers(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    resp_pers_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not (
        await verify_token_user_identity(
            caller_user=caller_user, roles=(settings.role.root,)
        )
        or await verify_is_i(caller_user=caller_user, user_id=resp_pers_id)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    resp_pers = await users_crud.get_any_user(
        session=session, any_user_id=resp_pers_id, role_id=settings.role.resp_pers
    )
    return resp_pers


@router.patch(
    f"{settings.api.full_update}{settings.api.resp_pers}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
        304: {"description": "User not modified"},
    },
)
async def full_right_update_resp_pers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    resp_pers_update: UserFullUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not (
        await verify_token_user_identity(
            caller_user=caller_user, roles=(settings.role.root,)
        )
        or await verify_is_i(caller_user=caller_user, user_id=resp_pers_update.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await users_crud.update_any_user(
        session=session,
        any_user_update=resp_pers_update,
    )


@router.patch(
    f"{settings.api.part_update}{settings.api.resp_pers}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
        304: {"description": "User not modified"},
    },
)
async def part_right_update_resp_pers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    resp_pers_update: UserPartUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not (
        await verify_token_user_identity(
            caller_user=caller_user, roles=(settings.role.root,)
        )
        or await verify_is_i(caller_user=caller_user, user_id=resp_pers_update.id)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await users_crud.update_any_user(
        session=session,
        any_user_update=resp_pers_update,
    )


@router.patch(
    f"{settings.api.self_update}{settings.api.resp_pers}",
    response_model=UserRead,
    responses={
        404: {"description": "User not found"},
        304: {"description": "User not modified"},
    },
)
async def self_update(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    resp_pers_self_update: UserSelfUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    resp_pers_update = UserPartUpdate(
        **resp_pers_self_update.model_dump(), id=caller_user.id
    )
    if not await verify_is_i(caller_user=caller_user, user_id=resp_pers_update.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await users_crud.update_any_user(
        session=session,
        any_user_update=resp_pers_update,
    )


@router.delete(f"{settings.api.delete}{settings.api.resp_pers}")
async def delete_resp_pers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
    resp_pers_id: int,
):
    if not (
        await verify_token_user_identity(
            caller_user=caller_user, roles=(settings.role.root,)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await users_crud.delete_any_user(
        session=session, any_user_id=resp_pers_id, role_id=settings.role.resp_pers
    )

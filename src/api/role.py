from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import role as roles_crud
from database import User, db_helper
from schemas.role import RoleCreate, RoleRead, RoleUpdate

from .validation import get_current_user_from_access_token, verify_token_user_identity

router = APIRouter(tags=["Role"])


@router.post(
    f"{settings.api.create}",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Role created"},
        403: {"description": "Not enough rights error"},
        422: {"description": "Validation error"},
    },
)
async def create_role(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    role_create: RoleCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    role = await roles_crud.create_role(
        session=session,
        role_create=role_create,
    )
    return role


@router.get(
    f"{settings.api.get}",
    response_model=RoleRead,
    responses={
        404: {"description": "Role not found"},
        403: {"description": "Not enough rights error"},
    },
)
async def get_role(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    role_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await roles_crud.get_role(session=session, role_id=role_id)


@router.patch(
    f"{settings.api.full_update}",
    response_model=RoleRead,
    responses={
        404: {"description": "Role not found"},
        304: {"description": "Role not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def update_role(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    role_update: RoleUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await roles_crud.update_role(session=session, role_update=role_update)


@router.delete(
    f"{settings.api.delete}/{{role_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Role not found"},
        403: {"description": "Not enough rights error"},
        204: {"description": "Role deleted successfully"},
    },
)
async def delete_role(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    role_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await roles_crud.delete_role(session=session, role_id=role_id)

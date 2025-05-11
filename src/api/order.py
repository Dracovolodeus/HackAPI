from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud import order as orders_crud
from database import User, db_helper
from schemas.order import (OrderCreate, OrderFullUpdate, OrderPartUpdate,
                           OrderRead)

from .validation import get_current_user_from_access_token, verify_token_user_identity

router = APIRouter(tags=["Order"])


@router.post(
    f"{settings.api.create}",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Order created"},
        422: {"description": "Validation error"},
        403: {"description": "Not enough rights error"},
    },
)
async def create_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_create: OrderCreate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    order = await orders_crud.create_order(
        session=session,
        order_create=order_create,
    )
    return order


@router.get(
    f"{settings.api.get}",
    response_model=OrderRead,
    responses={
        404: {"description": "Order not found"},
        403: {"description": "Not enough rights error"},
    },
)
async def get_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await orders_crud.get_order(session=session, order_id=order_id)


@router.patch(
    f"{settings.api.full_update}",
    response_model=OrderRead,
    responses={
        404: {"description": "Order not found"},
        304: {"description": "Order not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def full_rigth_update_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_update: OrderFullUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.root,)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await orders_crud.update_order(session=session, order_update=order_update)


@router.patch(
    f"{settings.api.part_update}",
    response_model=OrderRead,
    responses={
        404: {"description": "Order not found"},
        304: {"description": "Order not modified"},
        403: {"description": "Not enough rights error"},
    },
)
async def part_rigth_update_order(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    order_update: OrderPartUpdate,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user,
        roles=(
            settings.role.resp_pers,
            settings.role.root,
        ),
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await orders_crud.update_order(session=session, order_update=order_update)


@router.delete(
    f"{settings.api.delete}/{{order_id}}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Order not found"},
        204: {"description": "Order deleted successfully"},
        403: {"description": "Not enough rights error"},
    },
)
async def delete_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: int,
    caller_user: Annotated[User, Depends(get_current_user_from_access_token)],
):
    if not await verify_token_user_identity(
        caller_user=caller_user, roles=(settings.role.resp_pers, settings.role.root)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights error"
        )
    return await orders_crud.delete_order(session=session, order_id=order_id)

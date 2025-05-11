from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import Order
from schemas.order import OrderCreate, OrderFullUpdate, OrderPartUpdate
from utils.model import update_model


async def create_order(
    session: AsyncSession,
    order_create: OrderCreate,
) -> Order:
    """
    Create a new order and persist it to the database.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        order_create (OrderCreate): The data used to create the new order.

    Returns:
        Order: The created order instance after being added to the database.
    """

    # Creating an instanse of a database class
    order = Order(**order_create.model_dump())

    # Saving to the database
    session.add(order)
    await session.commit()
    await session.refresh(order)

    return order


async def get_order(
    session: AsyncSession,
    order_id: int,
) -> Order:
    """
    Retrieve an order by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        order_id (int): The ID of the order to retrieve.

    Returns:
        Order: The order instance if found.

    Raises:
        NotFoundError: If no order with the specified ID exists in the database.
    """

    order = await session.get(Order, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


async def update_order(
    session: AsyncSession, order_update: OrderPartUpdate | OrderFullUpdate
) -> Order:
    """
    Update an existing book's tag's data.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        order_update (OrderUpdate): The data containing updates for the order.

    Returns:
        Order: The updated order instance.

    Raises:
        NotFoundError: If the order to be updated does not exist.
        NotChangedError: If no changes are detected in the provided update data.
    """

    # Get the order
    order = await get_order(session, order_update.id)

    if not update_model(order_update, order):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )

    await session.commit()
    await session.refresh(order)
    return order


async def delete_order(session: AsyncSession, order_id: int) -> Order:
    """
    Delete an order by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        order_id (int): The ID of the order to delete.

    Returns:
        Order: The deleted order instance if found.

    Raises:
        NotFoundError: If no order with the specified ID exists in the database.
    """
    # Get the order
    order = await get_order(session, order_id)

    # Delete the order and save the changes
    await session.delete(order)
    await session.commit()
    return order

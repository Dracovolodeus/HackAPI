from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_refresh_token
from database.tables.user import User
from schemas.any_user import UserCreate, UserFullUpdate, UserPartUpdate
from utils.model import update_model


async def create_any_user(
    session: AsyncSession, any_user_create: UserCreate, role_id: int
) -> User:
    """
    Create a new book tag and persist it to the database.
    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        any_user_create (UserCreate): The data used to create the new book tag.
    Returns:
        User: The created book tag instance after being added to the database.
    Raises:
        HTTPException: If not enough rights or role not found
    """
    # Creating an instance of database class
    any_user = User(**any_user_create.model_dump(), role_id=role_id)

    session.add(any_user)
    await session.commit()
    any_user.refresh_token = create_refresh_token(any_user.id)

    # Saving to the database
    await session.commit()
    return any_user


async def get_any_user(
    session: AsyncSession, any_user_id: int, role_id: Optional[int] = None
) -> User:
    """
    Retrieve an user by their ID.
    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        any_user_id (int): The ID of the user to retrieve.
    Returns:
        User: The user instance if found.
    Raises:
        NotFoundError: If no user with the specified ID exists in the database.
    """
    any_user = await session.get(User, any_user_id)
    if any_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    elif role_id is not None and any_user.role_id != role_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong role")
    return any_user


async def update_any_user(
    session: AsyncSession,
    any_user_update: UserFullUpdate | UserPartUpdate,
) -> User:
    """
    Update an existing book's tag's data.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        any_user_update (UserFullUpdate): The data containing updates for the any_user.

    Returns:
        User: The updated any_user instance.

    Raises:
        NotFoundError: If the user to be updated does not exist.
        NotChangedError: If no changes are detected in the provided update data.
    """

    # Get the any_user
    any_user = await get_any_user(session, any_user_update.id)

    update_dict = any_user_update.model_dump(exclude_unset=True)
    if "new_id" in update_dict and update_dict["new_id"] == any_user.id:
        any_user.refresh_token = None

    if not update_model(any_user_update, any_user):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )

    await session.commit()
    await session.refresh(any_user)
    return any_user


async def delete_any_user(
    session: AsyncSession, any_user_id: int, role_id: int
) -> User:
    """
    Delete an any_user by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        any_user_id (int): The ID of the any_user to delete.

    Returns:
        User: The deleted any_user instance if found.

    Raises:
        NotFoundError: If no any_user with the specified ID exists in the database.
    """
    # Get the user
    any_user = await get_any_user(
        session=session, any_user_id=any_user_id, role_id=role_id
    )

    # Delete the any_user and save the changes
    await session.delete(any_user)
    await session.commit()
    return any_user

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import Role
from schemas.role import RoleCreate, RoleUpdate


async def create_role(
    session: AsyncSession,
    role_create: RoleCreate,
) -> Role:
    """
    Create a new role and persist it to the database.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        role_create (RoleCreate): The data used to create the new role.

    Returns:
        Role: The created role instance after being added to the database.
    """
    # Creating an instance of a database class
    role = Role(**role_create.model_dump())

    # Saving to the database
    session.add(role)
    await session.commit()
    await session.refresh(role)
    return role


async def get_role(session: AsyncSession, role_id: int) -> Role:
    """
    Retrieve a role by its ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        role_id (int): The ID of the role to retrieve.

    Returns:
        Role: The role instance if found.

    Raises:
        NotFoundError: If no role with the specified ID exists in the database.
    """
    role = await session.get(Role, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return role


async def update_role(session: AsyncSession, role_update: RoleUpdate) -> Role:
    """
    Updates role data.

    Args:
        session: Async database session
        role_update: Data for role update

    Returns:
        Updated role instance

    Raises:
        NotFoundError: If role not found
        NotChangedError: If no changes detected
    """
    # Get the role
    role = await get_role(session, role_update.id)

    # Checking if there are any changes
    if (role_update.new_id is None or role_update.new_id == role.id) and (
        role_update.name is None or role_update.name == role.name
    ):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )
    # Applying the changes
    if role_update.new_id is not None:
        role.id = role_update.new_id
    if role_update.name is not None:
        role.name = role_update.name

    await session.commit()
    await session.refresh(role)
    return role


async def delete_role(session: AsyncSession, role_id: int) -> Role:
    """
    Delete a role by its ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        role_id (int): The ID of the role to delete.

    Returns:
        Role: The deleted role instance if found.

    Raises:
        NotFoundError: If no role with the specified ID exists in the database.
    """
    # Get the role
    role = await get_role(session, role_id)

    # Delete the role and save the changes
    await session.delete(role)
    await session.commit()
    return role

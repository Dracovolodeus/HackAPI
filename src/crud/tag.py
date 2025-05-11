from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import Tag
from schemas.tag import TagCreate, TagFullUpdate, TagPartUpdate
from utils.model import update_model


async def create_tag(
    session: AsyncSession,
    tag_create: TagCreate,
) -> Tag:
    """
    Create a new book tag and persist it to the database.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        tag_create (TagCreate): The data used to create the new book tag.

    Returns:
        Tag: The created book tag instance after being added to the database.
    """

    # Creating an instance of a database class
    tag = Tag(**tag_create.model_dump())

    # Saving to the database
    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return tag


async def get_tag(session: AsyncSession, tag_id: int) -> Tag:
    """
    Retrieve an tag by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        tag_id (int): The ID of the tag to retrieve.

    Returns:
        Tag: The tag instance if found.

    Raises:
        NotFoundError: If no tag with the specified ID exists in the database.
    """
    tag = await session.get(Tag, tag_id)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag


async def update_tag(
    session: AsyncSession, tag_update: TagFullUpdate | TagPartUpdate
) -> Tag:
    """
    Update an existing book's tag's data.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        tag_update (TagUpdate): The data containing updates for the tag.

    Returns:
        Tag: The updated tag instance.

    Raises:
        NotFoundError: If the tag to be updated does not exist.
        NotChangedError: If no changes are detected in the provided update data.
    """

    # Get the tag
    tag = await get_tag(session, tag_update.id)

    if not update_model(tag_update, tag):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )

    await session.commit()
    await session.refresh(tag)
    return tag


async def delete_tag(session: AsyncSession, tag_id: int) -> Tag:
    """
    Delete an tag by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        tag_id (int): The ID of the tag to delete.

    Returns:
        Tag: The deleted tag instance if found.

    Raises:
        NotFoundError: If no tag with the specified ID exists in the database.
    """
    # Get the tag
    tag = await get_tag(session, tag_id)

    # Delete the tag and save the changes
    await session.delete(tag)
    await session.commit()
    return tag

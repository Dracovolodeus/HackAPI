from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import BookTag
from schemas.book_tag import (BookTagCreate, BookTagFullUpdate,
                              BookTagPartUpdate)
from utils.model import update_model


async def create_book_tag(
    session: AsyncSession,
    book_tag_create: BookTagCreate,
) -> BookTag:
    """
    Create a new book tag and persist it to the database.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_tag_create (BookTagCreate): The data used to create the new book tag.

    Returns:
        BookTag: The created book tag instance after being added to the database.
    """

    # Creating an instance of a database class
    book_tag = BookTag(**book_tag_create.model_dump())

    # Saving to the database
    session.add(book_tag)
    await session.commit()
    await session.refresh(book_tag)

    return book_tag


async def get_book_tag(session: AsyncSession, book_tag_id: int) -> BookTag:
    """
    Retrieve an book_tag by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_tag_id (int): The ID of the book_tag to retrieve.

    Returns:
        BookTag: The book_tag instance if found.

    Raises:
        NotFoundError: If no book_tag with the specified ID exists in the database.
    """
    book_tag = await session.get(BookTag, book_tag_id)
    if book_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="BookTag not found"
        )
    return book_tag


async def update_book_tag(
    session: AsyncSession, book_tag_update: BookTagFullUpdate | BookTagPartUpdate
) -> BookTag:
    """
    Update an existing book's tag's data.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_tag_update (BookTagUpdate): The data containing updates for the book_tag.

    Returns:
        BookTag: The updated book_tag instance.

    Raises:
        NotFoundError: If the book_tag to be updated does not exist.
        NotChangedError: If no changes are detected in the provided update data.
    """

    # Get the book_tag
    book_tag = await get_book_tag(session, book_tag_update.id)

    if not update_model(book_tag_update, book_tag):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )

    await session.commit()
    await session.refresh(book_tag)
    return book_tag


async def delete_book_tag(session: AsyncSession, book_tag_id: int) -> BookTag:
    """
    Delete an book_tag by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_tag_id (int): The ID of the book_tag to delete.

    Returns:
        BookTag: The deleted book_tag instance if found.

    Raises:
        NotFoundError: If no book_tag with the specified ID exists in the database.
    """
    # Get the book_tag
    book_tag = await get_book_tag(session, book_tag_id)

    # Delete the book_tag and save the changes
    await session.delete(book_tag)
    await session.commit()
    return book_tag

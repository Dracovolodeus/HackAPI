from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import Author
from schemas.author import AuthorCreate, AuthorFullUpdate, AuthorPartUpdate
from utils.model import update_model


async def create_author(
    session: AsyncSession,
    author_create: AuthorCreate,
) -> Author:
    """
    Create a new author and persist it to the database.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        author_create (AuthorCreate): The data used to create the new author.

    Returns:
        Author: The created author instance after being added to the database.
    """

    # Creating an instance of a database class
    author = Author(**author_create.model_dump())

    # Saving to the database
    session.add(author)
    await session.commit()
    await session.refresh(author)

    return author


async def get_author(
    session: AsyncSession,
    author_id: int,
) -> Author:
    """
    Retrieve an author by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        author_id (int): The ID of the author to retrieve.

    Returns:
        Author: The author instance if found.

    Raises:
        NotFoundError: If no author with the specified ID exists in the database.
    """

    author = await session.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found error"
        )
    return author


async def update_author(
    session: AsyncSession, author_update: AuthorPartUpdate | AuthorFullUpdate
) -> Author:
    """
    Update an existing author's data.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        author_update (AuthorUpdate): The data containing updates for the author.

    Returns:
        Author: The updated author instance.

    Raises:
        NotFoundError: If the author to be updated does not exist.
        NotChangedError: If no changes are detected in the provided update data.
    """

    # Get the author
    author = await get_author(session, author_update.id)

    if not update_model(author_update, author):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )
    await session.commit()
    await session.refresh(author)
    return author


async def delete_author(session: AsyncSession, author_id: int) -> Author:
    """
    Delete an author by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        author_id (int): The ID of the author to delete.

    Returns:
        Author: The deleted author instance if found.

    Raises:
        NotFoundError: If no author with the specified ID exists in the database.
    """
    # Get the author
    author = await get_author(session, author_id)

    # Delete the author and save the changes
    await session.delete(author)
    await session.commit()
    return author

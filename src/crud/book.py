from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import Book
from schemas.book import BookCreate, BookFullUpdate, BookPartUpdate
from utils.model import update_model


async def create_book(
    session: AsyncSession,
    book_create: BookCreate,
) -> Book:
    """
    Create a new author and persist it to the database.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_create (BookCreate): The data used to create the new book.

    Returns:
        Book: The created book instance after being added to the database.
    """

    # Creating an instance of a database class
    book = Book(**book_create.model_dump())

    # Saving to the database
    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


async def get_book(
    session: AsyncSession,
    book_id: int,
) -> Book:
    """
    Retrieve an book by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_id (int): The ID of the book to retrieve.

    Returns:
        Book: The book instance if found.

    Raises:
        NotFoundError: If no book with the specified ID exists in the database.
    """

    book = await session.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return book


async def update_book(
    session: AsyncSession,
    book_update: BookFullUpdate | BookPartUpdate,
) -> Book:
    """
    Update an existing book's data.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_update (BookUpdate): The data containing updates for the book.

    Returns:
        Book: The updated book  instance.

    Raises:
        NotFoundError: If the book to be updated does not exist.
        NotChangedError: If no changes are detected in the provided update data.
    """

    book = await get_book(session, book_update.id)

    if not update_model(book_update, book):
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="No changes detected"
        )

    await session.commit()
    await session.refresh(book)
    return book


async def delete_book(session: AsyncSession, book_id: int) -> Book:
    """
    Delete an book by their ID.

    Args:
        session (AsyncSession): The asynchronous database session to use for the operation.
        book_id (int): The ID of the book to delete.

    Returns:
        Book: The deleted book instance if found.

    Raises:
        NotFoundError: If no book with the specified ID exists in the database.
    """

    # Get the book
    book = await get_book(session, book_id)

    # Delete the role and save the changes
    await session.delete(book)
    await session.commit()
    return book

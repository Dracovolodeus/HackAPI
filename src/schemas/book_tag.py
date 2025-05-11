from typing import Optional

from pydantic import BaseModel


class BookTagBase(BaseModel):
    book_id: int
    tags: int


class BookTagCreate(BookTagBase): ...


class BookTagRead(BookTagBase): ...


class BookTagFullUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    book_id: Optional[int] = None
    tags: Optional[int] = None


class BookTagPartUpdate(BaseModel):
    id: int
    book_id: Optional[int] = None
    tags: Optional[int] = None

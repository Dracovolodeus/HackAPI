from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    name: str
    page_count: int
    year: int
    cover: str
    author_id: int


class BookCreate(BookBase): ...


class BookRead(BookBase):
    id: int


class BookFullUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    name: Optional[str] = None
    page_count: Optional[int] = None
    year: Optional[int] = None
    cover: Optional[str] = None
    author_id: Optional[int] = None


class BookPartUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    page_count: Optional[int] = None
    year: Optional[int] = None
    cover: Optional[str] = None
    author_id: Optional[int] = None

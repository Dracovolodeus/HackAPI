from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorCreate(AuthorBase): ...


class AuthorRead(AuthorBase):
    id: int


class AuthorFullUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AuthorPartUpdate(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None

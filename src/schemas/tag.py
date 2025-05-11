from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase): ...


class TagRead(TagBase):
    id: int


class TagFullUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    name: Optional[str] = None


class TagPartUpdate(BaseModel):
    id: int
    name: Optional[str] = None

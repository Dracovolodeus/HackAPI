from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase): ...


class RoleRead(RoleBase):
    id: int


class RoleUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    name: Optional[str] = None

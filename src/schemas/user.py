from typing import Optional

from pydantic import BaseModel, field_validator

from auth.utils import hash_password


class UserBase(BaseModel):
    first_name: str
    last_name: str
    second_name: str
    email: str
    password: str
    description: str
    birthday: str
    is_search: bool = False


class UserCreate(UserBase):

    @field_validator("password", mode="before")
    def set_password(cls, v):
        return hash_password(v)


class UserRead(UserBase):
    id: int
    description: str | None
    refresh_token: str | None


class UserPartRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    second_name: str
    description: str | None
    email: str

class UserLogin(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

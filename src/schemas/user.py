from typing import Optional

from pydantic import BaseModel, field_validator

from auth.utils import hash_password


class UserBase(BaseModel):
    first_name: str
    last_name: str
    second_name: str
    email: str
    telegram_id: int
    password: str
    phone: str


class UserCreate(UserBase):

    @field_validator("password", mode="before")
    def set_password(cls, v):
        return hash_password(v)


class UserCreateForAPI(UserBase): ...


class UserRead(UserBase):
    id: int
    role_id: int
    refresh_token: str


class UserFullUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[str] = None
    telegram_id: Optional[int] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[int] = None


class UserPartUpdate(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None


class UserSelfUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    telegram_id: Optional[int] = None

from datetime import date as dt_date
from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    book_id: int


class OrderCreate(OrderBase): ...


class OrderRead(OrderBase):
    id: int
    start_date: dt_date
    return_date: dt_date | None


class OrderFullUpdate(BaseModel):
    id: int
    new_id: Optional[int] = None
    start_date: Optional[dt_date] = None
    return_date: Optional[dt_date] = None
    user_id: Optional[int] = None
    book_id: Optional[int] = None


class OrderPartUpdate(BaseModel):
    id: int
    start_date: Optional[dt_date] = None
    return_date: Optional[dt_date] = None
    user_id: Optional[int] = None
    book_id: Optional[int] = None

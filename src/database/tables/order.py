from datetime import date as dt_date

from sqlalchemy import Date, ForeignKey, null
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Order(Base, IntIdPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    start_date: Mapped[dt_date] = mapped_column(Date, default=dt_date.today)
    return_date: Mapped[dt_date | None] = mapped_column(
        Date, default=None, server_default=null()
    )

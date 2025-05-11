from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class BookTag(Base, IntIdPkMixin):
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.id"),
    )
    tags: Mapped[int] = mapped_column(
        ForeignKey("tag.id"),
    )

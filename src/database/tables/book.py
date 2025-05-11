from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Book(Base, IntIdPkMixin):
    name: Mapped[str] = mapped_column(unique=True)
    page_count: Mapped[int]
    year: Mapped[int]
    cover: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

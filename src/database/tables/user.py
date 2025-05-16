from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin):

    # FCs
    first_name: Mapped[str]
    last_name: Mapped[str]
    second_name: Mapped[str]

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    refresh_token: Mapped[str | None] = mapped_column(nullable=True)

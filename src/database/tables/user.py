from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin):
    # FCs
    first_name: Mapped[str]
    last_name: Mapped[str]
    second_name: Mapped[str]
    birthday: Mapped[str]

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    refresh_token: Mapped[str | None] = mapped_column(nullable=True, default=None)

    description: Mapped[str | None] = mapped_column(nullable=True, default=None)
    is_search: Mapped[bool] = mapped_column(Boolean, default=False)

    want_join_to_team_ids: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(ARRAY(Integer())), default=list, server_default="{}"
    )

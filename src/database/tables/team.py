from sqlalchemy import (Boolean, Integer, String,  # Исправлен импорт String
                        Text)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Team(Base, IntIdPkMixin):
    name: Mapped[str]
    leader_id: Mapped[int] = mapped_column(Integer, index=True)
    idea: Mapped[str]
    idea_detail: Mapped[str]
    hackathon_id: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)

    teammates_ids: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(ARRAY(Integer())), default=list, server_default="{}"
    )

    need_roles: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String(100))),
        default=list,
        server_default="{}",
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, name="is_active", default=True)

    want_join_to_team_ids: Mapped[list[int]] = mapped_column(
        MutableList.as_mutable(ARRAY(Integer())), default=list, server_default="{}"
    )

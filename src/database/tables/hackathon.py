from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin
from sqlalchemy.dialects.postgresql import ARRAY


class Hackathon(Base, IntIdPkMixin):
    creator_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    organization_name: Mapped[str]
    contacts: Mapped[str]
    description: Mapped[str]
    detail: Mapped[list[dict[str, str]]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=lambda: [],
        nullable=False,
    )
    plan: Mapped[str]
    hackathon_name: Mapped[str]
    old_limitation: Mapped[int]
    email_text: Mapped[str]

    reg_start_date: Mapped[str]
    reg_end_date: Mapped[str]
    reg_limitation: Mapped[int]

    start_date: Mapped[str]
    end_date: Mapped[str]

    admins_ids: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(Integer)), default=lambda: [],
                                                  nullable=False,
                                                  )
    jury_ids: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(Integer)), default=lambda: [],
                                                nullable=False,
                                                )
    teams_ids: Mapped[list[int]] = mapped_column(MutableList.as_mutable(ARRAY(Integer)), default=lambda: [],
                                                 nullable=False,
                                                 )

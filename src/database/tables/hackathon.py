from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin
from sqlalchemy.dialects.postgresql import ARRAY


class Hackathon(Base, IntIdPkMixin):
    creator_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    organization_name: Mapped[str]
    contacts: Mapped[str]
    description: Mapped[str]
    plan: Mapped[str]
    hackathon_name: Mapped[str]
    old_limitation: Mapped[int]
    email_text: Mapped[str]

    reg_start_date: Mapped[str]
    reg_end_date: Mapped[str]
    reg_limitation: Mapped[int]

    start_date: Mapped[str]
    end_date: Mapped[str]

    admins_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    jury_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    teams_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))

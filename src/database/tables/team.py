from sqlalchemy.orm import Mapped

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Team(Base, IntIdPkMixin):
    name: Mapped[str]
    leader_id: Mapped[str]
    idea: Mapped[str]
    idea_detail: Mapped[str]

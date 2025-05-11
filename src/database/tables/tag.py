from sqlalchemy.orm import Mapped

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Tag(Base, IntIdPkMixin):
    name: Mapped[str]

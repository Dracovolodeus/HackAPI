from sqlalchemy.orm import Mapped

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Author(Base, IntIdPkMixin):
    first_name: Mapped[str]
    last_name: Mapped[str]

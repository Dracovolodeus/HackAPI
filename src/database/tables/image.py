from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins.int_id_pk import IntIdPkMixin


class Image(Base, IntIdPkMixin):
    data: Mapped[bytes] = mapped_column(LargeBinary)

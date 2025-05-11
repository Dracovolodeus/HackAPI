from sqlalchemy.orm import Mapped, mapped_column


class StrTokenUqMixin:
    token: Mapped[str] = mapped_column(unique=True)

from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base
from sqlalchemy import String, Boolean


class Users(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )

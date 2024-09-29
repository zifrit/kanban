from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import BYTEA


class Users(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[bytes] = mapped_column(BYTEA)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )

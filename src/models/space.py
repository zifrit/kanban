from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from .base_model import Base
from sqlalchemy import String


if TYPE_CHECKING:
    from src.models.user import Users


class Board(Base):
    __tablename__ = "board"
    name: Mapped[str] = mapped_column(String(255))
    user_is: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="boards")

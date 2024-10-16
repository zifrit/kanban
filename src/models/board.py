from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer
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
    columns: Mapped[list["Column"]] = relationship(back_populates="board")


class Column(Base):
    __tablename__ = "column"
    name: Mapped[str] = mapped_column(String(255))
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="columns")
    tasks: Mapped[list["Task"]] = relationship(back_populates="column")


class Task(Base):
    __tablename__ = "task"
    name: Mapped[str] = mapped_column(String(255))
    column_id: Mapped[int] = mapped_column(ForeignKey("column.id"))
    column: Mapped["Column"] = relationship(back_populates="tasks")
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["Users"] = relationship(back_populates="created_tasks")
    executor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    executor: Mapped["Users"] = relationship(back_populates="executable_tasks")

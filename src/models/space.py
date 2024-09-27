from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base
from sqlalchemy import String


class Space(Base):
    __tablename__ = "space"
    name: Mapped[str] = mapped_column(String(255))

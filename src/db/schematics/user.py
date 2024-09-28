from datetime import datetime

from pydantic import BaseModel, EmailStr
from src.db.schematics.base import BaseSchema


class BaseUser(BaseSchema):
    username: str
    email: EmailStr


class ShowUser(BaseUser):
    id: int


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseUser):
    username: str
    email: EmailStr


class ParticularUpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

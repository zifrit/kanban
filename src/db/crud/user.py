from src.db.db_connection import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, HTTPException, status, Path, Response
from sqlalchemy import Select
from src.models.user import Users
from src.db.schematics.user import (
    CreateUser,
    ShowUser,
    ParticularUpdateUser,
    UpdateUser,
)
import logging

logger = logging.getLogger(__name__)


async def get_users(session: AsyncSession) -> list[Users]:
    user = await session.scalars(Select(Users).order_by(Users.id))
    return list(user)


async def get_user(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.get_session),
) -> Users:
    user = await session.scalar(Select(Users).where(Users.id == user_id))
    return user


async def create_user(session: AsyncSession, user: CreateUser) -> Users:
    user = Users(**user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user: Users) -> None:
    user.is_active = False
    await session.commit()


async def update_user(
    session: AsyncSession,
    user: Users,
    user_schema: ParticularUpdateUser | UpdateUser,
    particular: bool = False,
) -> Users:
    for key, value in user_schema.model_dump(exclude_unset=particular).items():
        setattr(user, key, value)
    await session.commit()
    return user


async def user_activation(
    session: AsyncSession,
    user: Users,
):
    if user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already active"
        )
    user.is_active = True
    await session.commit()
    return {"message": "User activated"}

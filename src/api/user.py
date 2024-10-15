from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_connection import db_helper
from src.db.schematics.user import (
    ShowUser,
    CreateUser,
    ParticularUpdateUser,
    UpdateUser,
)
from src.db.crud import user as crud_user
import logging

from src.models import Users

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_model=list[ShowUser])
async def get_user(
    session: AsyncSession = Depends(db_helper.get_session),
) -> [ShowUser]:
    result = await crud_user.get_users(session)
    return result


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_user.create_user(session, user)


@router.post("/activate", status_code=status.HTTP_200_OK)
async def user_activation(
    user: Users = Depends(crud_user.get_user),
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_user.user_activation(session, user)


@router.get("/{user_id}", response_model=ShowUser)
async def get_user(
    user: ShowUser = Depends(crud_user.get_active_user),
) -> ShowUser:
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: Users = Depends(crud_user.get_user),
    session: AsyncSession = Depends(db_helper.get_session),
):
    await crud_user.delete_user(session, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def partial_update_user(
    user_schema: ParticularUpdateUser,
    user: Users = Depends(crud_user.get_user),
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_user.update_user(
        session=session, user=user, user_schema=user_schema, particular=True
    )


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
async def update_user(
    user_schema: UpdateUser,
    user: Users = Depends(crud_user.get_user),
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_user.update_user(
        session=session,
        user=user,
        user_schema=user_schema,
    )

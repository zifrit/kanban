from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_connection import db_helper
import logging

from src.db.schematics.column import (
    CreateColumnSchema,
    ShowColumnSchema,
    ParticularUpdateColumnSchema,
    UpdateColumnSchema,
)
from src.utils.auth_utils import get_current_active_user
from src.db.crud import column as crud_column

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=list[ShowColumnSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_columns(
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowColumnSchema:
    return await crud_column.get_columns(session)


@router.post(
    "/",
    response_model=ShowColumnSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def create_columns(
    column: CreateColumnSchema,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowColumnSchema:
    return await crud_column.create_column(session=session, column=column)


@router.get(
    "/{column_id}",
    response_model=ShowColumnSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_column(
    column_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowColumnSchema:
    return await crud_column.get_column_by_id(column_id=column_id, session=session)


@router.put(
    "/{column_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowColumnSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_column(
    column_id: int,
    column_schema: UpdateColumnSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_column.update_column(
        session=session,
        column_id=column_id,
        column_schema=column_schema,
    )


@router.patch(
    "/{column_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowColumnSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def particular_update_column(
    column_id: int,
    column_schema: ParticularUpdateColumnSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_column.update_column(
        session=session,
        column_id=column_id,
        column_schema=column_schema,
        particular=True,
    )


@router.delete(
    "{column_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_column(
    column_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    await crud_column.delete_column(column_id=column_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

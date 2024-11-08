from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_connection import db_helper
import logging

from src.db.schematics.column import (
    CreateColumnSchema,
    ShowColumnSchema,
    ShowColumnWithTasksSchema,
    ParticularUpdateColumnSchema,
    UpdateColumnSchema,
)
from src.utils.auth_utils import get_current_active_user
from src.db.crud.column import crud_column, get_column_tasks
from src.utils.raising_http_excp import RaiseHttpException

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
    return await crud_column.get(session=session)


@router.post(
    "/",
    response_model=ShowColumnSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def create_columns(
    column: CreateColumnSchema,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowColumnSchema:
    return await crud_column.create(session=session, obj_schema=column)


@router.get(
    "/{column_id}",
    response_model=ShowColumnSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_column(
    column_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowColumnSchema:
    return await crud_column.get_by_id(id_=column_id, session=session)


@router.get(
    "/{column_id}/tasks",
    response_model=ShowColumnWithTasksSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_column_with_tasks(
    column_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    result = await get_column_tasks(session, column_id)
    RaiseHttpException.check_is_exist(result)
    return result


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
    return await crud_column.update(
        session=session,
        id_=column_id,
        obj_schema=column_schema,
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
    return await crud_column.update(
        session=session,
        id_=column_id,
        obj_schema=column_schema,
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
    await crud_column.delete(id_=column_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

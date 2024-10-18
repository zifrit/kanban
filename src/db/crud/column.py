from datetime import timezone, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from src.models.board import Column
from src.db.schematics.column import (
    CreateColumnSchema,
    UpdateColumnSchema,
    ParticularUpdateColumnSchema,
)
import logging

from src.utils.raising_http_excp import RaiseHttpException

logger = logging.getLogger(__name__)


async def create_column(
    session: AsyncSession,
    column: CreateColumnSchema,
):
    column = Column(**column.model_dump())
    session.add(column)
    await session.commit()
    await session.refresh(column)
    return column


async def get_columns(
    session: AsyncSession,
):

    columns = await session.scalars(Select(Column).where(Column.deleted_at.is_(None)))
    return columns


async def get_column_by_id(
    session: AsyncSession,
    column_id: int,
):
    column = await session.scalar(
        Select(Column).where(Column.id == column_id, Column.deleted_at.is_(None))
    )
    RaiseHttpException.check_is_exist(column)
    return column


async def update_column(
    session: AsyncSession,
    column_id: int,
    column_schema: ParticularUpdateColumnSchema | UpdateColumnSchema,
    particular: bool = False,
):
    column = await get_column_by_id(session, column_id)
    for key, value in column_schema.model_dump(exclude_unset=particular).items():
        setattr(column, key, value)
    await session.commit()
    return column


async def delete_column(
    session: AsyncSession,
    column_id: int,
):
    column = await get_column_by_id(session, column_id)
    column.deleted_at = datetime.now(timezone.utc)
    await session.commit()

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud.base import ModelManager
from sqlalchemy import Select
from sqlalchemy.orm import selectinload
from src.models.board import Column, Task
from src.db.schematics.column import (
    CreateColumnSchema,
    UpdateColumnSchema,
    ShowColumnSchema,
    ParticularUpdateColumnSchema,
)
import logging


logger = logging.getLogger(__name__)


class ColumnManager(
    ModelManager[
        Column,
        ShowColumnSchema,
        CreateColumnSchema,
        UpdateColumnSchema,
        ParticularUpdateColumnSchema,
    ]
):
    pass


crud_column = ColumnManager(Column)


async def get_column_tasks(session: AsyncSession, id_: int) -> Column:
    return await session.scalar(
        Select(Column)
        .options(
            selectinload(Column.tasks.and_(Task.deleted_at.is_(None))).load_only(
                Task.executor_id,
                Task.id,
                Task.column_id,
                Task.name,
            )
        )
        .where(Column.id == id_, Column.deleted_at.is_(None))
    )

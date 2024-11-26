from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud.base import ModelManager
from sqlalchemy import select, exists, update
from fastapi import HTTPException, status
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
    async def delete(self, session: AsyncSession, id_: int, *args, **kwargs):
        await self.get_by_id(session, id_=id_)
        exists_query = await session.scalar(
            select(
                exists()
                .where(Column.id == Task.column_id, Column.id == id_)
                .where(Task.completed == False)
            )
        )
        if exists_query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The Column has unfinished tasks",
            )
        await session.execute(
            update(Column)
            .where(Column.id == id_)
            .values(deleted_at=datetime.now(timezone.utc))
        )
        await session.execute(
            update(Task)
            .where(Task.column_id == id_)
            .values(deleted_at=datetime.now(timezone.utc))
        )
        await session.commit()


crud_column = ColumnManager(Column)


async def get_column_tasks(session: AsyncSession, id_: int) -> Column:
    return await session.scalar(
        select(Column)
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

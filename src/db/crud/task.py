from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from src.db.crud.base import ModelManager
from src.models import Users
from src.models.board import Task
from src.db.schematics.task import (
    CreateTaskWithUserIDSchema,
    ShowTaskSchema,
    UpdateTaskSchema,
    ParticularUpdateTaskSchema,
)
import logging


logger = logging.getLogger(__name__)


class TaskManager(
    ModelManager[
        Task,
        ShowTaskSchema,
        CreateTaskWithUserIDSchema,
        UpdateTaskSchema,
        ParticularUpdateTaskSchema,
    ]
):
    pass


crud_task = TaskManager(Task)


async def get_user_task(
    session: AsyncSession,
    user: Users,
    created: bool = False,
    execute: bool = False,
    all_: bool = True,
    completed: bool = True,
):
    if execute:
        if all_:
            return await session.scalars(
                Select(Task).where(Task.executor_id == user.id)
            )
        else:
            return await session.scalars(
                Select(Task).where(
                    Task.executor_id == user.id,
                    Task.completed == completed,
                )
            )
    elif created:
        if all_:
            return await session.scalars(Select(Task).where(Task.creator_id == user.id))
        else:
            return await session.scalars(
                Select(Task).where(
                    Task.creator_id == user.id,
                    Task.completed == completed,
                )
            )
    else:
        raise HTTPException(status_code=404, detail="Task not found")

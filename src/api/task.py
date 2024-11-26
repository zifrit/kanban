from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_connection import db_helper
import logging

from src.models.user import Users
from src.models.board import Task, Column
from src.db.schematics.task import (
    CreateTaskSchema,
    CreateTaskWithUserIDSchema,
    ShowTaskSchema,
    UpdateTaskSchema,
    ParticularUpdateTaskSchema,
)
from src.utils.auth_utils import get_current_active_user
from src.db.crud.task import crud_task, get_user_task
from src.utils.raising_http_excp import RaiseHttpException

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=list[ShowTaskSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_tasks(
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowTaskSchema:
    return await crud_task.get(session=session)


@router.post(
    "/",
    response_model=ShowTaskSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def create_task(
    task_schema: CreateTaskSchema,
    user: Users = Depends(get_current_active_user),
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowTaskSchema:
    await RaiseHttpException.check_is_not_delete(
        session=session,
        _models={"Column": Column},
        _ids={"Column": task_schema.column_id},
    )
    task_schema.executor_id = (
        user.id if task_schema.executor_id is None else task_schema.executor_id
    )
    task_with_user_id = CreateTaskWithUserIDSchema(
        **task_schema.model_dump(), creator_id=user.id
    )
    return await crud_task.create(session=session, obj_schema=task_with_user_id)


@router.get(
    "/{task_id}",
    response_model=ShowTaskSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowTaskSchema:
    return await crud_task.get_by_id(id_=task_id, session=session)


@router.put(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowTaskSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_task(
    task_id: int,
    task_schema: UpdateTaskSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    await RaiseHttpException.check_is_not_delete(
        session=session,
        _models={"Column": Column},
        _ids={"Column": task_schema.column_id},
    )
    return await crud_task.update(
        session=session,
        id_=task_id,
        obj_schema=task_schema,
    )


@router.patch(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowTaskSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def particular_update_task(
    task_id: int,
    task_schema: ParticularUpdateTaskSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    if task_schema.column_id:
        await RaiseHttpException.check_is_not_delete(
            session=session,
            _models={"Column": Column},
            _ids={"Column": task_schema.column_id},
        )
    return await crud_task.update(
        session=session,
        id_=task_id,
        obj_schema=task_schema,
        particular=True,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    await crud_task.delete(id_=task_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/user/created",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowTaskSchema],
)
async def get_user_created_task(
    completed: bool = False,
    all_: bool = True,
    session: AsyncSession = Depends(db_helper.get_session),
    user: Users = Depends(get_current_active_user),
):
    """
    ## Возвращается список задач, которые создал пользователь
    ### Параметры:
        при all_ = True: Возвращает все задачи и выполненные и не выполненные и игнорирует completed
        при completed = True и all_ = False: Возвращает только выполненные
        при completed = False и all_ = False: Возвращает только не выполненные
    ### Возвращает:
        200 OK: JSON с задачами
    """
    return await get_user_task(
        session=session,
        user=user,
        all_=all_,
        completed=completed,
        created=True,
    )


@router.get(
    "/user/execute",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowTaskSchema],
)
async def get_user_execute_task(
    completed: bool = False,
    all_: bool = True,
    session: AsyncSession = Depends(db_helper.get_session),
    user: Users = Depends(get_current_active_user),
):
    """
    ## Возвращается список задач, где пользователь назначен исполнителем
    ### Параметры:
        при all_ = True: Возвращает все задачи и выполненные и не выполненные и игнорирует completed
        при completed = True и all_ = False: Возвращает только выполненные
        при completed = False и all_ = False: Возвращает только не выполненные
    ### Возвращает:
        200 OK: JSON с задачами
    """
    return await get_user_task(
        session=session,
        user=user,
        all_=all_,
        completed=completed,
        execute=True,
    )

from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, update
from sqlalchemy.orm import selectinload
from src.db.crud.base import ModelManager
from src.models.board import Board, Column, Task
from src.models.user import Users
from src.db.schematics.board import (
    CreateBoardWithUserIDSchema,
    UpdateBoardSchema,
    ShowBoardSchema,
    ParticularUpdateBoardSchema,
)
import logging


logger = logging.getLogger(__name__)


class BoardManager(
    ModelManager[
        Board,
        ShowBoardSchema,
        CreateBoardWithUserIDSchema,
        UpdateBoardSchema,
        ParticularUpdateBoardSchema,
    ]
):
    async def delete(self, session: AsyncSession, id_: int, *args, **kwargs):
        board = await self.get_by_id(session, id_=id_)
        exists_query = await session.scalar(
            select(
                exists()
                .where(Column.id == Task.column_id, Column.board_id == id_)
                .where(Task.completed == False)
            )
        )
        if exists_query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The board has unfinished tasks",
            )
        columns = await session.scalars(select(Column).where(Column.board_id == id_))
        columns = list(columns)
        columns_ids = [column.id for column in columns]
        for column in columns:
            column.deleted_at = datetime.now(timezone.utc)
        await session.execute(
            update(Task)
            .where(Task.column_id.in_(columns_ids))
            .values(deleted_at=datetime.now(timezone.utc))
        )
        board.deleted_at = datetime.now(timezone.utc)
        await session.commit()


crud_board = BoardManager(Board)


async def get_user_boards(
    session: AsyncSession,
    user: Users,
):

    boards = await session.scalars(
        select(Board).where(Board.user_id == user.id, Board.deleted_at.is_(None))
    )
    return boards


async def get_board_columns(session: AsyncSession, id_: int) -> Board:
    return await session.scalar(
        select(Board)
        .options(selectinload(Board.columns.and_(Column.deleted_at.is_(None))))
        .where(Board.id == id_, Board.deleted_at.is_(None))
    )

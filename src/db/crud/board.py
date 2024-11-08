from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from sqlalchemy.orm import selectinload
from src.db.crud.base import ModelManager
from src.models.board import Board, Column
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
    pass


crud_board = BoardManager(Board)


async def get_user_boards(
    session: AsyncSession,
    user: Users,
):

    boards = await session.scalars(
        Select(Board).where(Board.user_id == user.id, Board.deleted_at.is_(None))
    )
    return boards


async def get_board_columns(session: AsyncSession, id_: int) -> Board:
    return await session.scalar(
        Select(Board)
        .options(selectinload(Board.columns.and_(Column.deleted_at.is_(None))))
        .where(Board.id == id_, Board.deleted_at.is_(None))
    )

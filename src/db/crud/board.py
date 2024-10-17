from datetime import timezone, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from src.models.board import Board
from src.models.user import Users
from src.db.schematics.board import (
    CreateBoardSchema,
    UpdateBoardSchema,
    ParticularUpdateBoardSchema,
)
import logging

from src.utils.raising_http_excp import RaiseHttpException

logger = logging.getLogger(__name__)


async def create_board(
    session: AsyncSession,
    user: Users,
    board: CreateBoardSchema,
):
    board = Board(**board.model_dump(), user_id=user.id)
    session.add(board)
    await session.commit()
    await session.refresh(board)
    return board


async def get_boards(
    session: AsyncSession,
):

    boards = await session.scalars(Select(Board), Board.deleted_at.is_(None))
    return boards


async def get_user_boards(
    session: AsyncSession,
    user: Users,
):

    boards = await session.scalars(
        Select(Board).where(Board.user_id == user.id, Board.deleted_at.is_(None))
    )
    return boards


async def get_board_by_id(
    session: AsyncSession,
    board_id: int,
):
    board = await session.scalar(
        Select(Board).where(Board.id == board_id, Board.deleted_at.is_(None))
    )
    RaiseHttpException.check_is_exist(board)
    return board


async def update_board(
    session: AsyncSession,
    board_id: int,
    board_schema: ParticularUpdateBoardSchema | UpdateBoardSchema,
    particular: bool = False,
):
    board = await get_board_by_id(session, board_id)
    for key, value in board_schema.model_dump(exclude_unset=particular).items():
        setattr(board, key, value)
    await session.commit()
    return board


async def delete_board(
    session: AsyncSession,
    board_id: int,
):
    board = await get_board_by_id(session, board_id)
    board.deleted_at = datetime.now(timezone.utc)
    await session.commit()

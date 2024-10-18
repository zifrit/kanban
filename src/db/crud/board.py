from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from src.db.crud.base import ModelManager
from src.models.board import Board
from src.models.user import Users
from src.db.schematics.board import (
    CreateBoardWithUserIDSchema,
    UpdateBoardSchema,
    ShowBoardSchema,
    ParticularUpdateBoardSchema,
)
import logging


logger = logging.getLogger(__name__)


class ColumnManager(
    ModelManager[
        Board,
        ShowBoardSchema,
        CreateBoardWithUserIDSchema,
        UpdateBoardSchema,
        ParticularUpdateBoardSchema,
    ]
):
    pass


crud_board = ColumnManager(Board)


async def get_user_boards(
    session: AsyncSession,
    user: Users,
):

    boards = await session.scalars(
        Select(Board).where(Board.user_id == user.id, Board.deleted_at.is_(None))
    )
    return boards

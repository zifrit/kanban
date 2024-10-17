from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_connection import db_helper
import logging

from src.models import Users
from src.db.schematics.board import (
    CreateBoardSchema,
    ShowBoardSchema,
    ParticularUpdateBoardSchema,
    UpdateBoardSchema,
)
from src.utils.auth_utils import get_current_active_user
from src.db.crud import board as crud_board

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=list[ShowBoardSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_boards(
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowBoardSchema:
    return await crud_board.get_boards(session)


@router.get(
    "/users",
    response_model=list[ShowBoardSchema],
)
async def get_user_boards(
    session: AsyncSession = Depends(db_helper.get_session),
    user: Users = Depends(get_current_active_user),
) -> list[ShowBoardSchema]:
    return await crud_board.get_user_boards(session, user=user)


@router.post("/", response_model=ShowBoardSchema)
async def create_board(
    board: CreateBoardSchema,
    session: AsyncSession = Depends(db_helper.get_session),
    user: Users = Depends(get_current_active_user),
) -> ShowBoardSchema:
    return await crud_board.create_board(session=session, user=user, board=board)


@router.get(
    "/{board_id}",
    response_model=ShowBoardSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_board(
    board_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowBoardSchema:
    return await crud_board.get_board_by_id(board_id=board_id, session=session)


@router.put(
    "/{board_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBoardSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_user(
    board_id: int,
    board_schema: UpdateBoardSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_board.update_board(
        session=session,
        board_id=board_id,
        board_schema=board_schema,
    )


@router.patch(
    "/{board_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBoardSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_user(
    board_id: int,
    board_schema: ParticularUpdateBoardSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_board.update_board(
        session=session,
        board_id=board_id,
        board_schema=board_schema,
        particular=True,
    )


@router.delete(
    "{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_board(
    board_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    await crud_board.delete_board(board_id=board_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

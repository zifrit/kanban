from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_connection import db_helper
import logging

from src.models import Users
from src.db.schematics.board import (
    CreateBoardSchema,
    CreateBoardWithUserIDSchema,
    ShowBoardSchema,
    ParticularUpdateBoardSchema,
    UpdateBoardSchema,
)
from src.utils.auth_utils import get_current_active_user
from src.db.crud.board import crud_board, get_user_boards as user_boards

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
    return await crud_board.get(session=session)


@router.get(
    "/users",
    response_model=list[ShowBoardSchema],
)
async def get_user_boards(
    session: AsyncSession = Depends(db_helper.get_session),
    user: Users = Depends(get_current_active_user),
) -> list[ShowBoardSchema]:
    return await user_boards(session, user=user)


@router.post("/", response_model=ShowBoardSchema)
async def create_board(
    board: CreateBoardSchema,
    session: AsyncSession = Depends(db_helper.get_session),
    user: Users = Depends(get_current_active_user),
) -> ShowBoardSchema:
    board_with_user_id = CreateBoardWithUserIDSchema(
        **board.model_dump(), user_id=user.id
    )
    return await crud_board.create(session=session, obj_schema=board_with_user_id)


@router.get(
    "/{board_id}",
    response_model=ShowBoardSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def get_board(
    board_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ShowBoardSchema:
    return await crud_board.get_by_id(id_=board_id, session=session)


@router.put(
    "/{board_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBoardSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_board(
    board_id: int,
    board_schema: UpdateBoardSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_board.update(
        session=session,
        id_=board_id,
        obj_schema=board_schema,
    )


@router.patch(
    "/{board_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBoardSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def particular_update_board(
    board_id: int,
    board_schema: ParticularUpdateBoardSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud_board.update(
        session=session,
        id_=board_id,
        obj_schema=board_schema,
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
    await crud_board.delete(id_=board_id, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

import logging
from fastapi import Depends, APIRouter, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from pydantic import BaseModel
from src.db.db_connection import db_helper
from src.db.crud import user as crud_users
from src.utils import auth_utils

router = APIRouter()

logger = logging.getLogger(__name__)


class UserLogin(BaseModel):
    username: str
    password: str


async def validate_auth_user(
    login_user: UserLogin,
    session: AsyncSession = Depends(db_helper.get_session),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username or password incorrect",
    )
    user = await crud_users.get_user_by_username(
        session=session, username=login_user.username
    )
    if not user:
        raise unauthed_exception
    if not (auth_utils.check_password(login_user.password, user.password)):
        raise unauthed_exception
    if not user.is_active:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not active",
        )
    return user


@router.post("/login")
async def login(
    user=Depends(validate_auth_user),
):
    payload = {
        "sub": user.username,
    }
    token = auth_utils.create_jwt_token(payload=payload)
    return {"token": token}

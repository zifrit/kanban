from datetime import timedelta, datetime

import bcrypt
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.crud import user as crud_user
from src.core.settings import settings
from src.db.db_connection import db_helper
from src.models import Users

http_bearer = HTTPBearer(auto_error=True)


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def create_jwt_token(
    payload: dict,
    key: str = settings.CRYPTO_SECRET_KEY,
    algorithm: str = settings.CRYPTO_ALGORITHM,
    access_expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
):
    data = payload.copy()
    now = datetime.utcnow()
    expires = now + timedelta(minutes=access_expire_minutes)
    data.update(
        exp=expires,
        iat=now,
        type="access_token",
    )
    access_token = jwt.encode(
        payload=data,
        key=key,
        algorithm=algorithm,
    )
    return access_token


def decode_token(
    token: str | bytes,
    key: str = settings.CRYPTO_SECRET_KEY,
    algorithm: str = settings.CRYPTO_ALGORITHM,
):
    encode = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[algorithm],
    )
    return encode


async def get_current_user(
    session: AsyncSession = Depends(db_helper.get_session),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    try:
        payload = decode_token(token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user = await crud_user.get_user_by_username(payload["sub"], session=session)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )


async def get_current_active_user(
    user: Users = Depends(get_current_user),
):
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

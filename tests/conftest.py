import asyncio
import pytest
import pytest_asyncio
from sqlalchemy import Select

from src.core.settings import settings
from src.db.db_connection import db_helper
from src.models.user import Users
from httpx import AsyncClient, ASGITransport
from main import app
from src.utils.auth_utils import hash_password


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        base_url=settings.HOST_URL, transport=ASGITransport(app=app)
    ) as ac:
        yield ac


user_token = {}


@pytest_asyncio.fixture(scope="function")
async def get_token(async_client):
    async with db_helper.session_factory() as session:
        admin_user = await session.scalar(
            Select(Users).where(Users.username == "admin")
        )
        if not admin_user:
            admin_user = Users(
                username="admin",
                password=hash_password("admin"),
                email="admin@example.com",
            )
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)
        if user_token.get(admin_user.username, False):
            yield f"Bearer {user_token[admin_user.username]}"
        else:
            data = {
                "username": "admin",
                "password": "admin",
            }
            url = f"{settings.HOST_URL}/jwt/login"
            response = await async_client.post(url, json=data)
            response = response.json()
            user_token[admin_user.username] = response["token"]
            yield f"Bearer {response['token']}"


@pytest_asyncio.fixture
async def make_get_request(get_token, async_client):
    async def inner(
        path: str,
        query_params: dict | None = {},
    ):
        response = await async_client.get(
            path,
            params=query_params,
            headers={"Authorization": get_token},
        )
        return response

    return inner


@pytest_asyncio.fixture
async def make_post_request(get_token, async_client):
    async def inner(
        path: str,
        json: dict | None,
        query_params: dict | None = {},
    ):
        response = await async_client.post(
            path,
            json=json,
            params=query_params,
            headers={"Authorization": get_token},
        )
        return response

    return inner


@pytest_asyncio.fixture
async def make_put_request(get_token, async_client):
    async def inner(
        path: str,
        json: dict | None = {},
        query_params: dict | None = {},
    ):
        response = await async_client.put(
            path,
            json=json,
            params=query_params,
            headers={"Authorization": get_token},
        )
        return response

    return inner


@pytest_asyncio.fixture
async def make_patch_request(get_token, async_client):
    async def inner(
        path: str,
        json: dict | None = {},
        query_params: dict | None = {},
    ):
        response = await async_client.patch(
            path,
            json=json,
            params=query_params,
            headers={"Authorization": get_token},
        )
        return response

    return inner


@pytest_asyncio.fixture
async def make_delete_request(get_token, async_client):
    async def inner(
        path: str,
    ):
        response = await async_client.delete(
            path,
            headers={"Authorization": get_token},
        )
        return response

    return inner

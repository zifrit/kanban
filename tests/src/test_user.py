import http
import pytest


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/",
                "data": {
                    "username": "string1",
                    "password": "string1",
                    "email": "user@example.com",
                },
            },
            {
                "response": {
                    "username": "string1",
                    "email": "user@example.com",
                    "id": 2,
                },
                "status": http.HTTPStatus.CREATED,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_crete_user(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_post_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/",
                "data": {
                    "username": "string1",
                    "password": "string1",
                    "email": "user@example.com",
                },
            },
            {
                "response": {"detail": "User with this username already exists"},
                "status": http.HTTPStatus.BAD_REQUEST,
            },
        ),
        (
            {
                "search": "/api/users/",
                "data": {
                    "username": "string2",
                    "password": "string1",
                    "email": "user@example.com",
                },
            },
            {
                "response": {"detail": "User with this email already exists"},
                "status": http.HTTPStatus.BAD_REQUEST,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_duplicate_crete_user(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_post_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/",
            },
            {
                "response": [
                    {
                        "username": "admin",
                        "email": "admin@example.com",
                        "id": 1,
                    },
                    {
                        "username": "string1",
                        "email": "user@example.com",
                        "id": 2,
                    },
                ],
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_users(
    make_get_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_get_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/1",
            },
            {
                "response": {
                    "username": "admin",
                    "email": "admin@example.com",
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_user(
    make_get_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_get_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/10000",
            },
            {
                "response": {"detail": "User not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_invalid_user(
    make_get_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_get_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
            },
            {
                "status": http.HTTPStatus.NO_CONTENT,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_user(
    make_delete_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_delete_request(path=query["search"])
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/10000",
            },
            {
                "response": {"detail": "User not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_invalid_user(
    make_delete_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_delete_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "username": "string1",
                    "email": "user1@example.com",
                },
            },
            {
                "response": {
                    "username": "string1",
                    "email": "user1@example.com",
                    "id": 2,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_user(
    make_put_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_put_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "username": "admin",
                    "email": "user1@example.com",
                },
            },
            {
                "response": {"detail": "User with this username already exists"},
                "status": http.HTTPStatus.BAD_REQUEST,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_update_user(
    make_put_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_put_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "email": "user1@example.com",
                },
            },
            {
                "response": {
                    "detail": [
                        {
                            "type": "missing",
                            "loc": ["body", "username"],
                            "msg": "Field required",
                            "input": {"email": "user1@example.com"},
                        }
                    ]
                },
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_user_with_missing_username(
    make_put_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_put_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "username": "string1",
                },
            },
            {
                "response": {
                    "detail": [
                        {
                            "type": "missing",
                            "loc": ["body", "email"],
                            "msg": "Field required",
                            "input": {"username": "string1"},
                        }
                    ]
                },
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_user_with_missing_email(
    make_put_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_put_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "username": "string2",
                },
            },
            {
                "response": {
                    "username": "string2",
                    "email": "user1@example.com",
                    "id": 2,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_particular_update_user_username(
    make_patch_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_patch_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "email": "user2@example.com",
                },
            },
            {
                "response": {
                    "username": "string2",
                    "email": "user2@example.com",
                    "id": 2,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_particular_update_user_email(
    make_patch_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_patch_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/users/2",
                "data": {
                    "email": "admin@example.com",
                },
            },
            {
                "response": {"detail": "User with this email already exists"},
                "status": http.HTTPStatus.BAD_REQUEST,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_particular_update_user(
    make_patch_request,
    query: dict,
    expected_answer: dict,
):
    """checking for duplication when particular updating"""
    response = await make_patch_request(path=query["search"], json=query["data"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]

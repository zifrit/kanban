import http
import pytest


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/board/",
                "data": {
                    "name": "Board_1",
                },
            },
            {
                "response": {
                    "name": "Board_1",
                    "user_id": 1,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/board/",
                "data": {
                    "name": "Board_2",
                },
            },
            {
                "response": {
                    "name": "Board_2",
                    "user_id": 1,
                    "id": 2,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/board/",
                "data": {
                    "name": "Board_3",
                },
            },
            {
                "response": {
                    "name": "Board_3",
                    "user_id": 1,
                    "id": 3,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_board(
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
                "search": "/api/board/",
                "data": {
                    "name": 1,
                },
            },
            {
                "response": "Input should be a valid string",
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_board(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_post_request(path=query["search"], json=query["data"])
    assert response.json()["detail"][0]["msg"] == expected_answer["response"]
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/board/",
            },
            {
                "response": [
                    {
                        "name": "Board_1",
                        "user_id": 1,
                        "id": 1,
                    },
                    {
                        "name": "Board_2",
                        "user_id": 1,
                        "id": 2,
                    },
                    {
                        "name": "Board_3",
                        "user_id": 1,
                        "id": 3,
                    },
                ],
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_board(
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
                "search": "/api/board/users",
            },
            {
                "response": [
                    {
                        "name": "Board_1",
                        "user_id": 1,
                        "id": 1,
                    },
                    {
                        "name": "Board_2",
                        "user_id": 1,
                        "id": 2,
                    },
                    {
                        "name": "Board_3",
                        "user_id": 1,
                        "id": 3,
                    },
                ],
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_user_board(
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
                "search": "/api/board/1",
            },
            {
                "response": {
                    "name": "Board_1",
                    "user_id": 1,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_board_by_id(
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
                "search": "/api/board/1000",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_get_board_by_id(
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
                "search": "/api/board/1",
                "data": {"name": "New_Board_1"},
            },
            {
                "response": {
                    "name": "New_Board_1",
                    "user_id": 1,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_board(
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
                "search": "/api/board/1",
                "data": {"name": 1},
            },
            {
                "response": [
                    {"field": "name", "error": "Input should be a valid string"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "search": "/api/board/1",
                "data": {"other_field": "Board_1"},
            },
            {
                "response": [
                    {"field": "name", "error": "Field required"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "search": "/api/board/1",
                "data": {},
            },
            {
                "response": [
                    {"field": "name", "error": "Field required"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_update_board(
    make_put_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_put_request(path=query["search"], json=query["data"])
    assert (
        response.json()["detail"][0]["msg"] == expected_answer["response"][0]["error"]
    )
    assert (
        response.json()["detail"][0]["loc"][1]
        == expected_answer["response"][0]["field"]
    )
    assert response.status_code == expected_answer["status"]


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/board/1",
                "data": {"name": "New_Board_1_"},
            },
            {
                "response": {
                    "name": "New_Board_1_",
                    "user_id": 1,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/board/1",
                "data": {},
            },
            {
                "response": {
                    "name": "New_Board_1_",
                    "user_id": 1,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_particular_update_board(
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
                "search": "/api/board/1",
            },
            {
                "status": http.HTTPStatus.NO_CONTENT,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_board(
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
                "search": "/api/board/1",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_again_board(
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
                "search": "/api/board/1000",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_delete_board(
    make_delete_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_delete_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]

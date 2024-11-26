import http
import pytest


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/column/",
                "data": {
                    "name": "Column_1",
                    "board_id": 2,
                },
            },
            {
                "response": {
                    "name": "Column_1",
                    "board_id": 2,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/column/",
                "data": {
                    "name": "Column_2",
                    "board_id": 2,
                },
            },
            {
                "response": {
                    "name": "Column_2",
                    "board_id": 2,
                    "id": 2,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/column/",
                "data": {
                    "name": "Column_3",
                    "board_id": 2,
                },
            },
            {
                "response": {
                    "name": "Column_3",
                    "board_id": 2,
                    "id": 3,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_column(
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
                "search": "/api/column/",
                "data": {"board_id": 2},
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
                "search": "/api/column/",
                "data": {
                    "name": 1,
                    "board_id": 2,
                },
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
                "search": "/api/column/",
                "data": {"name": "Column_3"},
            },
            {
                "response": [
                    {"field": "board_id", "error": "Field required"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "search": "/api/column/",
                "data": {
                    "name": "Column_3",
                    "board_id": "asd",
                },
            },
            {
                "response": [
                    {
                        "field": "board_id",
                        "error": "Input should be a valid integer, unable to parse string as an integer",
                    },
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_column(
    make_post_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_post_request(path=query["search"], json=query["data"])
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
                "search": "/api/column/",
                "data": {
                    "name": "Column_3",
                    "board_id": 21222,
                },
            },
            {
                "response": {"detail": [{"Board": "Not exist"}]},
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        )
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_column_2(
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
                "search": "/api/column/",
            },
            {
                "response": [
                    {"name": "Column_1", "board_id": 2, "id": 1},
                    {"name": "Column_2", "board_id": 2, "id": 2},
                    {"name": "Column_3", "board_id": 2, "id": 3},
                ],
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_columns(
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
                "search": "/api/column/1",
            },
            {
                "response": {
                    "name": "Column_1",
                    "board_id": 2,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/column/2",
            },
            {
                "response": {
                    "name": "Column_2",
                    "board_id": 2,
                    "id": 2,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_column_by_id(
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
                "search": "/api/column/100000",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        )
    ],
)
@pytest.mark.asyncio
async def test_invalid_get_column_by_id(
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
                "search": "/api/column/1",
                "data": {
                    "name": "Update_Column_1",
                    "board_id": 2,
                },
            },
            {
                "response": {
                    "name": "Update_Column_1",
                    "board_id": 2,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_column(
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
                "search": "/api/column/1",
                "data": {
                    "board_id": 2,
                },
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
                "search": "/api/column/1",
                "data": {"name": "Update_Column_1"},
            },
            {
                "response": [
                    {"field": "board_id", "error": "Field required"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "search": "/api/column/1",
                "data": {
                    "name": 123,
                    "board_id": 2,
                },
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
                "search": "/api/column/1",
                "data": {
                    "name": "123",
                    "board_id": "asdw",
                },
            },
            {
                "response": [
                    {
                        "field": "board_id",
                        "error": "Input should be a valid integer, unable to parse string as an integer",
                    },
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_update_column(
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
                "search": "/api/column/1",
                "data": {"name": "Particular_Update_Column_1"},
            },
            {
                "response": {
                    "name": "Particular_Update_Column_1",
                    "board_id": 2,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/column/1",
                "data": {"board_id": 3},
            },
            {
                "response": {
                    "name": "Particular_Update_Column_1",
                    "board_id": 3,
                    "id": 1,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_particular_update_column(
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
                "search": "/api/column/1",
                "data": {
                    "name": 123,
                    "board_id": 2,
                },
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
                "search": "/api/column/1",
                "data": {
                    "name": "123",
                    "board_id": "asdw",
                },
            },
            {
                "response": [
                    {
                        "field": "board_id",
                        "error": "Input should be a valid integer, unable to parse string as an integer",
                    },
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_particular_update_column(
    make_patch_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_patch_request(path=query["search"], json=query["data"])
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
                "search": "/api/column/1",
            },
            {
                "status": http.HTTPStatus.NO_CONTENT,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_column(
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
                "search": "/api/column/1",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_again_column(
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
                "search": "/api/column/1000",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_delete_column(
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
                "search": "/api/board/2/column",
            },
            {
                "response": {
                    "name": "Board_2",
                    "columns": [
                        {"name": "Column_2", "board_id": 2, "id": 2},
                        {"name": "Column_3", "board_id": 2, "id": 3},
                    ],
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_board_columns(
    make_get_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_get_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]

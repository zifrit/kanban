import http
import pytest


@pytest.mark.parametrize(
    "query, expected_answer",
    [
        (
            {
                "search": "/api/task/",
                "data": {
                    "name": "Task_1",
                    "column_id": 2,
                },
            },
            {
                "response": {
                    "name": "Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 1,
                    "creator_id": 1,
                    "completed": False,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/task/",
                "data": {
                    "name": "Task_2",
                    "column_id": 2,
                },
            },
            {
                "response": {
                    "name": "Task_2",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 2,
                    "creator_id": 1,
                    "completed": False,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_task(
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
                "search": "/api/task/",
                "data": {"column_id": 2},
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
                "search": "/api/task/",
                "data": {
                    "name": 1,
                    "column_id": 2,
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
                "search": "/api/task/",
                "data": {"name": "Task_3"},
            },
            {
                "response": [
                    {"field": "column_id", "error": "Field required"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "search": "/api/task/",
                "data": {
                    "name": "Task_3",
                    "column_id": "asd",
                },
            },
            {
                "response": [
                    {
                        "field": "column_id",
                        "error": "Input should be a valid integer, unable to parse string as an integer",
                    },
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_task(
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
                "search": "/api/task/",
                "data": {
                    "name": "Task_3",
                    "column_id": 21222,
                },
            },
            {
                "response": {"detail": [{"Column": "Not exist"}]},
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        )
    ],
)
@pytest.mark.asyncio
async def test_invalid_create_task_2(
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
                "search": "/api/task/",
            },
            {
                "response": [
                    {
                        "name": "Task_1",
                        "column_id": 2,
                        "executor_id": 1,
                        "id": 1,
                        "creator_id": 1,
                        "completed": False,
                    },
                    {
                        "name": "Task_2",
                        "column_id": 2,
                        "executor_id": 1,
                        "id": 2,
                        "creator_id": 1,
                        "completed": False,
                    },
                ],
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_tasks(
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
                "search": "/api/task/1",
            },
            {
                "response": {
                    "name": "Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 1,
                    "creator_id": 1,
                    "completed": False,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/task/2",
            },
            {
                "response": {
                    "name": "Task_2",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 2,
                    "creator_id": 1,
                    "completed": False,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_task_by_id(
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
                "search": "/api/task/100000",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        )
    ],
)
@pytest.mark.asyncio
async def test_invalid_get_task_by_id(
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
                "search": "/api/task/1",
                "data": {
                    "name": "Update_Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "completed": False,
                },
            },
            {
                "response": {
                    "name": "Update_Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 1,
                    "creator_id": 1,
                    "completed": False,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/task/1",
                "data": {
                    "name": "Update_Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "completed": True,
                },
            },
            {
                "response": {
                    "name": "Update_Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 1,
                    "creator_id": 1,
                    "completed": True,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_task(
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
                "search": "/api/task/1",
                "data": {
                    "column_id": 2,
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
                "search": "/api/task/1",
                "data": {"name": "Update_Task_1"},
            },
            {
                "response": [
                    {"field": "column_id", "error": "Field required"},
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "search": "/api/task/1",
                "data": {
                    "name": 123,
                    "column_id": 2,
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
                "search": "/api/task/1",
                "data": {
                    "name": "123",
                    "column_id": "asdw",
                },
            },
            {
                "response": [
                    {
                        "field": "column_id",
                        "error": "Input should be a valid integer, unable to parse string as an integer",
                    },
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_update_task(
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
                "search": "/api/task/1",
                "data": {"name": "Particular_Update_Task_1"},
            },
            {
                "response": {
                    "name": "Particular_Update_Task_1",
                    "column_id": 2,
                    "executor_id": 1,
                    "id": 1,
                    "creator_id": 1,
                    "completed": True,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
        (
            {
                "search": "/api/task/1",
                "data": {"column_id": 3},
            },
            {
                "response": {
                    "name": "Particular_Update_Task_1",
                    "column_id": 3,
                    "executor_id": 1,
                    "id": 1,
                    "creator_id": 1,
                    "completed": True,
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_particular_update_task(
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
                "search": "/api/task/1",
                "data": {
                    "name": 123,
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
                "search": "/api/task/1",
                "data": {
                    "column_id": "asdw",
                },
            },
            {
                "response": [
                    {
                        "field": "column_id",
                        "error": "Input should be a valid integer, unable to parse string as an integer",
                    },
                ],
                "status": http.HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_particular_update_task(
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
                "search": "/api/task/1",
            },
            {
                "status": http.HTTPStatus.NO_CONTENT,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_task(
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
                "search": "/api/task/1",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_again_task(
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
                "search": "/api/task/1000",
            },
            {
                "response": {"detail": "Not found"},
                "status": http.HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_invalid_delete_task(
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
                "search": "/api/column/2/tasks",
            },
            {
                "response": {
                    "name": "Column_2",
                    "board_id": 2,
                    "tasks": [
                        {
                            "name": "Task_2",
                            "column_id": 2,
                            "executor_id": 1,
                            "id": 2,
                        }
                    ],
                },
                "status": http.HTTPStatus.OK,
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_column_task(
    make_get_request,
    query: dict,
    expected_answer: dict,
):
    response = await make_get_request(path=query["search"])
    assert response.json() == expected_answer["response"]
    assert response.status_code == expected_answer["status"]

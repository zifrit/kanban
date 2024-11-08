from src.db.schematics.base import BaseSchema


class TaskSchema(BaseSchema):
    name: str
    column_id: int
    executor_id: int | None = None


class CreateTaskSchema(TaskSchema):
    pass


class CreateTaskWithUserIDSchema(TaskSchema):
    creator_id: int


class UpdateTaskSchema(TaskSchema):
    completed: bool


class ParticularUpdateTaskSchema(TaskSchema):
    name: str | None = None
    column_id: int | None = None
    executor_id: int | None = None
    completed: bool | None = None


class ShowTaskSchema(TaskSchema):
    id: int
    creator_id: int
    completed: bool

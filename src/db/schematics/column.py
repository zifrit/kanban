from src.db.schematics.base import BaseSchema
from src.db.schematics.task import ShortShowTaskSchema


class ColumnSchema(BaseSchema):
    name: str
    board_id: int


class CreateColumnSchema(ColumnSchema):
    pass


class UpdateColumnSchema(ColumnSchema):
    pass


class ParticularUpdateColumnSchema(ColumnSchema):
    name: str | None = None
    board_id: int | None = None


class ShowColumnSchema(ColumnSchema):
    id: int


class ShortShowColumnSchema(ColumnSchema):
    id: int


class ShowColumnWithTasksSchema(ColumnSchema):
    tasks: list[ShortShowTaskSchema] | None = None

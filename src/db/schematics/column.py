from src.db.schematics.base import BaseSchema


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

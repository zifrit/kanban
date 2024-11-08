from src.db.schematics.base import BaseSchema
from src.db.schematics.column import ShortShowColumnSchema


class BoardSchema(BaseSchema):
    name: str


class CreateBoardSchema(BoardSchema):
    pass


class CreateBoardWithUserIDSchema(BoardSchema):
    user_id: int


class UpdateBoardSchema(BoardSchema):
    pass


class ParticularUpdateBoardSchema(BoardSchema):
    name: str | None = None


class ShowBoardSchema(BoardSchema):
    user_id: int
    id: int


class ShowBoarWithColumnSchema(BoardSchema):
    columns: list[ShortShowColumnSchema] | None = None

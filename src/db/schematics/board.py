from src.db.schematics.base import BaseSchema


class BoardSchema(BaseSchema):
    name: str


class CreateBoardSchema(BoardSchema):
    pass


class UpdateBoardSchema(BoardSchema):
    pass


class ParticularUpdateBoardSchema(BoardSchema):
    name: str | None = None


class ShowBoardSchema(BoardSchema):
    user_id: int
    id: int

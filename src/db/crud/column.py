from src.db.crud.base import ModelManager
from src.models.board import Column
from src.db.schematics.column import (
    CreateColumnSchema,
    UpdateColumnSchema,
    ShowColumnSchema,
    ParticularUpdateColumnSchema,
)
import logging


logger = logging.getLogger(__name__)


class ColumnManager(
    ModelManager[
        Column,
        ShowColumnSchema,
        CreateColumnSchema,
        UpdateColumnSchema,
        ParticularUpdateColumnSchema,
    ]
):
    pass


crud_column = ColumnManager(Column)

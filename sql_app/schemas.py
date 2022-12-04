from pydantic import BaseModel

from api.dto.metrics import AbstractDimensionDTO
from enums.dimension import DimensionEnum


class Dimension(AbstractDimensionDTO):
    id: int
    title: DimensionEnum
    resource_id: int

    class Config:
        orm_mode = True


class Resource(BaseModel):
    id: int
    title: str
    team_id: int

    dimensions: list[Dimension] = []

    class Config:
        orm_mode = True


class Team(BaseModel):
    id: int | None
    title: str | None

    resources: list[Resource] = []

    class Config:
        orm_mode = True

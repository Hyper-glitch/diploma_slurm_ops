from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel

from enums.decision import DecisionEnum
from enums.dimension import DimensionEnum
from enums.usage import UsageEnum


class AbstractDimensionDTO(BaseModel):
    mean: float
    median: float
    usage_type: UsageEnum
    intensity: str
    decision: DecisionEnum
    collect_date: str


class DimensionDTO(BaseModel):
    __root__: Dict[str, AbstractDimensionDTO]

    @classmethod
    def prepare_dimension_dto(cls, dimension: dict[str, Any]) -> DimensionDTO:
        __root__ = None

        for key, values in dimension.items():
            abc_dto = AbstractDimensionDTO(
                mean=values["mean"],
                median=values["median"],
                usage_type=values["usage_type"],
                intensity=values["intensity"],
                decision=values["decision"],
                collect_date=values["collect_date"],
            )

            match key:
                case DimensionEnum.CPU.value:
                    __root__ = {DimensionEnum.CPU.value: abc_dto}
                case DimensionEnum.RAM.value:
                    __root__ = {DimensionEnum.RAM.value: abc_dto}
                case DimensionEnum.NETFLOW.value:
                    __root__ = {DimensionEnum.NETFLOW.value: abc_dto}
                case _:
                    raise Exception(f"Unexpected dimension: {key}")

        return cls(__root__=__root__)


class DimensionsDTO(BaseModel):
    dimensions: list[DimensionDTO]


class ResourceDTO(BaseModel):
    __root__: Dict[str, DimensionsDTO]

    @classmethod
    def prepare_resource_dto(
        cls, resource: str, dimensions: DimensionsDTO
    ) -> ResourceDTO:
        return cls(__root__={resource: dimensions})


class ResourcesDTO(BaseModel):
    resources: list[ResourceDTO]


class TeamResponse(BaseModel):
    __root__: Dict[str, ResourcesDTO]

    @classmethod
    def prepare_team_dto(cls, team: str, resources: ResourcesDTO) -> TeamResponse:
        return cls(__root__={team: resources})


class TeamsResponse(BaseModel):
    teams: list[TeamResponse]

    @staticmethod
    def prepare_teams_dto(
        data: dict[str, dict[str, list[dict[str, dict]]]]
    ) -> list[TeamResponse]:
        teams_dto: list[TeamResponse] = []

        for team, resources in data.items():
            resources_dto: list[ResourceDTO] = []

            for resource, dimensions in resources.items():
                dimensions_dto: list[DimensionDTO] = []

                for dimension in dimensions:
                    if dimension is None:
                        continue

                    dimensions_dto.append(
                        DimensionDTO.prepare_dimension_dto(dimension=dimension)
                    )

                resources_dto.append(
                    ResourceDTO.prepare_resource_dto(
                        resource=resource,
                        dimensions=DimensionsDTO(dimensions=dimensions_dto),
                    )
                )
            teams_dto.append(
                TeamResponse.prepare_team_dto(
                    team=team,
                    resources=ResourcesDTO(resources=resources_dto),
                )
            )

        return teams_dto

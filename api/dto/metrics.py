from typing import Dict, Any

from pydantic import BaseModel

from enums.analyzer import UsageEnum, DimensionEnum


class ABCDimensionDTO(BaseModel):
    mean: float
    median: float
    usage_type: UsageEnum
    intensity: str
    decision: str
    collect_date: str


class DimensionDTO(BaseModel):
    __root__: Dict[str, ABCDimensionDTO]


class DimensionsDTO(BaseModel):
    dimensions: list[DimensionDTO]


class ResourceDTO(BaseModel):
    __root__: Dict[str, DimensionsDTO]


class ResourcesDTO(BaseModel):
    resources: list[ResourceDTO]


class TeamDTO(BaseModel):
    __root__: Dict[str, ResourcesDTO]


class TeamsDTO(BaseModel):
    teams: list[TeamDTO]


class AnalyzedMetricsDTO(BaseModel):
    teams: list[TeamDTO]

    @staticmethod
    def prepare_nested_dto(data) -> list[TeamDTO]:
        teams_dto: list[TeamDTO] = []

        for team, resources in data.items():
            resources_dto: list[ResourceDTO] = []

            for resource, dimensions in resources.items():
                dimensions_dto: list[DimensionDTO] = []

                for dimension in dimensions:
                    if dimension is None:
                        continue

                    dimensions_dto.append(
                        AnalyzedMetricsDTO.prepare_dimension_dto(
                            dimension=dimension
                        )
                    )

                resources_dto.append(
                    AnalyzedMetricsDTO.prepare_resource_dto(
                        resource=resource, dimensions=DimensionsDTO(dimensions=dimensions_dto),
                    )
                )
            teams_dto.append(AnalyzedMetricsDTO.prepare_team_dto(
                team=team, resources=ResourcesDTO(resources=resources_dto),
            ))

        return teams_dto

    @staticmethod
    def prepare_dimension_dto(dimension: dict[str, Any]) -> DimensionDTO:
        for key, values in dimension.items():
            abc_dto = ABCDimensionDTO(
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

            return DimensionDTO(__root__=__root__)

    @staticmethod
    def prepare_resource_dto(resource: str, dimensions: DimensionsDTO) -> ResourceDTO:
        return ResourceDTO(__root__={resource: dimensions})

    @staticmethod
    def prepare_team_dto(team: str, resources: ResourcesDTO) -> TeamDTO:
        return TeamDTO(__root__={team: resources})

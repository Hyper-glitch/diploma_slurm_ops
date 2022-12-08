import logging
from typing import Any

from analyze_service.parser import ResourceParser

logger = logging.getLogger("resource_analyzer")


def handle_raw_data(raw_data: str):
    logger.info("Starting to analyze resource data.")
    analyzed_data: dict[str, dict[str, list[dict[str, dict[str, Any]]]]] = {}

    splitted_commands = raw_data.split("$")

    for splitted_command in splitted_commands:
        parsed_data = splitted_command.split("|")
        team = parsed_data[0]
        parsed_resources = parsed_data[1].split(";")
        analyze_raw_data(
            analyzed_data=analyzed_data,
            team=team,
            raw_data=parsed_resources,
        )

    logger.info("Successfully analyzed resource data.")
    return analyzed_data


def analyze_raw_data(analyzed_data, team, raw_data):
    analyzed_resources = {}
    step = 200
    analyzed_dimensions: list[dict[str, Any]] = []

    for data_amount in range(0, 6000, step):
        resources = raw_data[data_amount: data_amount + step]
        try:
            parser_instance = ResourceParser(team=team, resources=resources)
        except ZeroDivisionError:
            analyzed_dimensions.append(None)
        else:
            analyzed_dimensions.append(
                parser_instance.analyzed_data[team][parser_instance.resource_id]
            )
        finally:
            if (data_amount + step) % 600 == 0:
                analyzed_resources.update(
                    {parser_instance.resource_id: analyzed_dimensions}
                )
                analyzed_dimensions = []

    analyzed_data[team] = analyzed_resources

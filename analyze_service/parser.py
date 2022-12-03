"""Module for resource parser."""
from enums.analyzer import IntensityEnum, UsageEnum, DecisionEnum


class ResourceParser:
    """Class for resource parser."""
    __slots__ = (
        'dimension', 'resource_id', 'median', 'mean', 'team', 'resources', 'load_values', 'analyzed_data',
        'usage_type', 'intensity', 'decision', 'collect_date'
    )

    def __init__(self, team, resources):
        self.collect_date = None
        self.load_values = None
        self.dimension = None
        self.resource_id = None
        self.team = team
        self.resources = resources
        self.get_resource_values()
        self.analyzed_data = self.analyze_data()
        self.decision = self.make_decision()

    def get_resource_values(self):
        resource = self.resources[0]

        if isinstance(resource, str):
            resource_id, dimension, load_values, collect_date = self.parse_http_values()
        else:
            resource_id, dimension, load_values, collect_date = self.parse_db_values()

        self.resource_id = resource_id
        self.dimension = dimension
        self.load_values = load_values
        self.collect_date = collect_date

    def parse_http_values(self):
        load_values = []
        last_index = len(self.resources) - 1

        for idx, parsed_resource in enumerate(self.resources):
            resource_values = parsed_resource.lstrip('(').rstrip(')').split(',')
            load_values.append(int(resource_values[-1]))
            if idx == last_index:
                collect_date = resource_values[-2].split()[0]

        resource_id = resource_values[0]
        dimension = resource_values[1]
        return resource_id, dimension, load_values, collect_date

    def parse_db_values(self):
        load_values = []
        last_index = len(self.resources) - 1

        for idx, parsed_resource in enumerate(self.resources):
            load_values.append(int(parsed_resource[-2]))
            if idx == last_index:
                collect_date = parsed_resource[-1]

        _, resource_id, dimension, _, _ = parsed_resource
        return resource_id, dimension, load_values, collect_date

    def analyze_data(self):
        setattr(self, 'mean', self.get_mean())
        setattr(self, 'median', self.get_median())
        setattr(self, 'usage_type', self.define_usage_type())
        setattr(self, 'intensity', self.define_intensity())

        return {
            self.team: {
                self.resource_id:
                    {
                        self.dimension: {
                            'mean': round(self.mean, 2),
                            'median': round(self.median, 2),
                            'usage_type': self.usage_type,
                            'intensity': self.intensity,
                            'decision': self.make_decision(),
                            'collect_date': self.collect_date,
                        }
                    }
            }
        }

    def get_mean(self) -> float:
        """Calculate the average of values.

        Returns:
            average - is a single number taken as representative of a list of numbers.
        """
        return sum(self.load_values) / len(self.load_values)

    def get_median(self) -> float:
        """Calculate the median of values.

        Returns:
            median - median is the value separating the higher half from the lower half of a data sample.
        """
        quotient, remainder = divmod(len(self.load_values), 2)
        return self.load_values[quotient] if remainder else sum(self.load_values[quotient - 1:quotient + 1]) / 2

    def define_usage_type(self) -> str:
        """Compute and define service load."""

        min_decreased_percentage = 0.75
        min_increased_percentage = 1.25
        fraction = self.mean / self.median

        if fraction > min_increased_percentage:
            return UsageEnum.RACES
        elif fraction < min_decreased_percentage:
            return UsageEnum.DECREASE
        return UsageEnum.STABLE

    def define_intensity(self):
        match self.median:
            case float() if 0 < self.median <= 30:
                return IntensityEnum.LOW.value
            case float() if 30 < self.median <= 60:
                return IntensityEnum.MEDIUM.value
            case float() if 60 < self.median <= 90:
                return IntensityEnum.HIGH.value
            case float() if self.median > 90:
                return IntensityEnum.EXTREME.value

    def make_decision(self):
        usage_types = UsageEnum.values()
        text = None

        if self.intensity == IntensityEnum.LOW.value and self.usage_type in usage_types:
            text = DecisionEnum.DELETE.value
        elif self.intensity == IntensityEnum.MEDIUM.value and self.usage_type == UsageEnum.DECREASE.value:
            text = DecisionEnum.DELETE.value
        elif self.intensity == IntensityEnum.MEDIUM.value and self.usage_type in usage_types[:-1]:
            text = DecisionEnum.NORMAL.value
        elif self.intensity == IntensityEnum.HIGH.value and self.usage_type in usage_types[1:]:
            text = DecisionEnum.NORMAL.value
        elif self.intensity == IntensityEnum.HIGH.value and self.usage_type == UsageEnum.RACES.value:
            text = DecisionEnum.EXTEND.value
        elif self.intensity == IntensityEnum.EXTREME.value and self.usage_type in UsageEnum.values():
            text = DecisionEnum.EXTEND.value

        return text

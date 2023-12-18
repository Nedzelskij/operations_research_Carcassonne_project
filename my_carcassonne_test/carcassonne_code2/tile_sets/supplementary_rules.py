from enum import Enum


class SupplementaryRule(Enum):
    FARMERS = "farmers"

    def to_json(self):
        return self.value

    def __str__(self):
        return self.value
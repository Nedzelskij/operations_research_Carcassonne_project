from enum import Enum


class TileSet(Enum):
    BASE = "base"
    THE_RIVER = "the_river"

    def to_json(self):
        return self.value

    def __str__(self):
        return self.value
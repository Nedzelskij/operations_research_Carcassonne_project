import random
from typing import Optional

from carcassonne_code2.objects.actions.meeple_action import MeepleAction
from carcassonne_code2.objects.actions.tile_action import TileAction
from carcassonne_code2.objects.coordinate import Coordinate
from carcassonne_code2.objects.game_phase import GamePhase
from carcassonne_code2.objects.tile import Tile
from carcassonne_code2.tile_sets.base_deck import base_tile_counts, base_tiles
from carcassonne_code2.tile_sets.supplementary_rules import SupplementaryRule
from carcassonne_code2.tile_sets.the_river_deck import the_river_tiles, the_river_tile_counts
from carcassonne_code2.tile_sets.tile_sets import TileSet


class CarcassonneGameState:

    def __init__(
            self,
            tile_sets: [TileSet] = (TileSet.BASE, TileSet.THE_RIVER),
            supplementary_rules: [SupplementaryRule] = (SupplementaryRule.FARMERS),
            players: int = 2,
            board_size: (int, int) = (40, 40),
            starting_position: Coordinate = Coordinate(11, 24)
    ):
        self.deck = self.initialize_deck(tile_sets=tile_sets)
        self.supplementary_rules: [SupplementaryRule] = supplementary_rules
        self.board: [[Tile]] = [[None for column in range(board_size[1])] for row in range(board_size[0])]
        self.starting_position: Coordinate = starting_position
        self.next_tile = self.deck.pop(0)
        self.players = players
        self.meeples = [7 for _ in range(players)]
        self.placed_meeples = [[] for _ in range(players)]
        self.scores: [float] = [0 for _ in range(players)]
        self.current_player = 0
        self.phase = GamePhase.TILES
        self.last_tile_action: Optional[TileAction] = None
        self.computer_action_priority: float = -100
        self.final_computer_tile_action: TileAction = None
        self.final_computer_meeple_action: MeepleAction = None

    def get_tile(self, row: int, column: int):
        if row < 0 or column < 0:
            return None
        elif row >= len(self.board) or column >= len(self.board[0]):
            return None
        else:
            return self.board[row][column]

    def empty_board(self):
        for row in self.board:
            for column in row:
                if column is not None:
                    return False
        return True

    def is_terminated(self) -> bool:
        return self.next_tile is None
    
    def initialize_deck(self, tile_sets: [TileSet]):
        deck: [Tile] = []

        if TileSet.THE_RIVER in tile_sets:
            deck.append(the_river_tiles["river_start"])

            new_tiles = []
            for card_name, count in the_river_tile_counts.items():
                if card_name == "river_start":
                    continue
                if card_name == "river_end":
                    continue

                for i in range(count):
                    new_tiles.append(the_river_tiles[card_name])

            random.shuffle(new_tiles)
            for tile in new_tiles:
                deck.append(tile)

            deck.append(the_river_tiles["river_end"])

        new_tiles = []

        if TileSet.BASE in tile_sets:
            for card_name, count in base_tile_counts.items():
                for i in range(count):
                    new_tiles.append(base_tiles[card_name])

        random.shuffle(new_tiles)
        for tile in new_tiles:
            deck.append(tile)

        return deck
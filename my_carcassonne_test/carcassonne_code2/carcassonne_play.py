from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.carcassonne_representer import CarcassonneRepresenter
from carcassonne_code2.objects.actions.action import Action
from carcassonne_code2.tile_sets.supplementary_rules import SupplementaryRule
from carcassonne_code2.tile_sets.tile_sets import TileSet
from carcassonne_code2.utils.action_util import ActionUtil
from carcassonne_code2.utils.state_updater import StateUpdater
from carcassonne_code2.objects.tile import Tile
from carcassonne_code2.utils.tile_position_finder import TilePositionFinder
from carcassonne_code2.utils.possible_move_finder import PossibleMoveFinder

class CarcassonnePlay:

    def __init__(self,
                 players: int = 2,
                 tile_sets: [TileSet] = (TileSet.BASE, TileSet.THE_RIVER),
                 supplementary_rules: [SupplementaryRule] = (SupplementaryRule.FARMERS)):
        self.players = players
        self.tile_sets = tile_sets
        self.supplementary_rules = supplementary_rules
        self.state: CarcassonneGameState = CarcassonneGameState(
            tile_sets=tile_sets,
            players=players,
            supplementary_rules=supplementary_rules
        )
        self.visualiser = CarcassonneRepresenter()

    def set_initial_tile(self):
        initial_action = ActionUtil.get_initial_tile(self.state)
        self.state = StateUpdater.apply_initial_action(game_state=self.state, action=initial_action)
        self.render()

    def reset(self):
        self.state = CarcassonneGameState(tile_sets=self.tile_sets, supplementary_rules=self.supplementary_rules)

    def step(self, player: int, action: Action):
        self.state = StateUpdater.apply_action(game_state=self.state, action=action)

    def render(self):
        self.visualiser.draw_game_state(self.state)

    def is_finished(self) -> bool:
        return self.state.is_terminated()

    def get_current_player(self) -> int:
        return self.state.current_player

    def get_possible_actions(self) -> [Action]:
        return ActionUtil.get_possible_actions(self.state)
    
    def check_player_tile_action(self, tile_to_play: Tile, row_index: int, column_index: int, tile_turns: int) -> bool:
        return TilePositionFinder.check_tile_actions(self.state, tile_to_play, row_index, column_index, tile_turns)
    
    def get_player_tile_action(self, row_index: int, column_index: int, tile_turns: int) -> Action:
        return ActionUtil.get_tile_action(self.state, row_index, column_index, tile_turns)
    
    def check_player_meeple_action(self, meeple_action : tuple) -> bool:
        return PossibleMoveFinder.check_meeple_actions(self.state, meeple_action)

    def get_player_meeple_action(self, meeple_action : tuple) -> Action:
        return ActionUtil.get_meeple_action(self.state, meeple_action)
    
    def get_computer_action(self) -> Action:
        return ActionUtil.get_computer_tile_meeple_action(self.state)

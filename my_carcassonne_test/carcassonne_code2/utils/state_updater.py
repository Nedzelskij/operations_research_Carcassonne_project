import copy

from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.objects.actions.action import Action
from carcassonne_code2.objects.actions.meeple_action import MeepleAction
from carcassonne_code2.objects.actions.pass_action import PassAction
from carcassonne_code2.objects.actions.tile_action import TileAction
from carcassonne_code2.objects.game_phase import GamePhase
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.meeple_type import MeepleType
from carcassonne_code2.utils.points_collector import PointsCollector


class StateUpdater:

    @staticmethod
    def next_player(game_state: CarcassonneGameState) -> CarcassonneGameState:
        game_state.phase = GamePhase.TILES
        game_state.current_player = game_state.current_player + 1
        if game_state.current_player >= game_state.players:
            game_state.current_player = 0
        return game_state

    @staticmethod
    def play_tile(game_state: CarcassonneGameState, tile_action: TileAction) -> CarcassonneGameState:
        game_state.board[tile_action.coordinate.row][tile_action.coordinate.column] = tile_action.tile
        game_state.phase = GamePhase.MEEPLES
        game_state.last_tile_action = tile_action
        return game_state
    
    @staticmethod
    def play_current_tile(game_state: CarcassonneGameState, tile_action: TileAction):
        game_state.board[tile_action.coordinate.row][tile_action.coordinate.column] = tile_action.tile
        game_state.last_tile_action = tile_action
    
    @staticmethod
    def play_initial_tile(game_state: CarcassonneGameState, tile_action: TileAction) -> CarcassonneGameState:
        game_state.board[tile_action.coordinate.row][tile_action.coordinate.column] = tile_action.tile
        game_state.last_tile_action = tile_action
        return game_state
    
    @staticmethod
    def play_current_meeple(game_state: CarcassonneGameState, meeple_action: MeepleAction) -> CarcassonneGameState:
        game_state.placed_meeples[game_state.current_player].append(
                MeeplePosition(meeple_type=meeple_action.meeple_type,
                               coordinate_with_side=meeple_action.coordinate_with_side))

    @staticmethod
    def clear_current_tile_action(game_state: CarcassonneGameState, tile_action: TileAction):
        game_state.board[tile_action.coordinate.row][tile_action.coordinate.column] = None
        game_state.fake_last_tile_action = None

    @staticmethod
    def play_meeple(game_state: CarcassonneGameState, meeple_action: MeepleAction) -> CarcassonneGameState:
        game_state.placed_meeples[game_state.current_player].append(
                MeeplePosition(meeple_type=meeple_action.meeple_type,
                               coordinate_with_side=meeple_action.coordinate_with_side))

        if meeple_action.meeple_type == MeepleType.NORMAL or meeple_action.meeple_type == MeepleType.FARMER:
            game_state.meeples[game_state.current_player] += 1 if meeple_action.remove else -1

        return game_state

    @staticmethod
    def draw_tile(game_state: CarcassonneGameState) -> CarcassonneGameState:
        if len(game_state.deck) == 0:
            game_state.next_tile = None
        else:
            game_state.next_tile = game_state.deck.pop(0)
        return game_state

    @staticmethod
    def remove_meeples_and_update_score(game_state: CarcassonneGameState) -> CarcassonneGameState:
        if game_state.last_tile_action is not None and game_state.last_tile_action.tile is not None:
            PointsCollector.remove_meeples_and_collect_points(game_state=game_state,
                                                              coordinate=game_state.last_tile_action.coordinate)
        return game_state

    @classmethod
    def apply_action(cls, game_state: CarcassonneGameState, action: Action) -> CarcassonneGameState:
        new_game_state: CarcassonneGameState = copy.deepcopy(game_state)

        if isinstance(action, TileAction):
            cls.play_tile(game_state=new_game_state, tile_action=action)
            new_game_state.phase = GamePhase.MEEPLES
        elif isinstance(action, MeepleAction):
            cls.play_meeple(game_state=new_game_state, meeple_action=action)
        elif isinstance(action, PassAction):
            if game_state.phase == GamePhase.TILES:
                cls.draw_tile(game_state=new_game_state)
                new_game_state.phase = GamePhase.MEEPLES
            elif game_state.phase == GamePhase.MEEPLES:
                pass

        if game_state.phase == GamePhase.MEEPLES:
            cls.remove_meeples_and_update_score(game_state=new_game_state)
            cls.draw_tile(game_state=new_game_state)
            cls.next_player(game_state=new_game_state)

        if new_game_state.is_terminated():
            PointsCollector.count_final_scores(game_state=new_game_state)

        return new_game_state
    
    @classmethod
    def apply_initial_action(cls, game_state: CarcassonneGameState, action: Action) -> CarcassonneGameState:
        new_game_state: CarcassonneGameState = copy.deepcopy(game_state)

        cls.play_initial_tile(game_state=new_game_state, tile_action=action)
        cls.draw_tile(game_state=new_game_state)

        return new_game_state
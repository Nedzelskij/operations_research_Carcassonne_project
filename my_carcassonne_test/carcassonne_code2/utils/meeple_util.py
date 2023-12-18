from typing import Optional

from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.objects.coordinate_with_side import CoordinateWithSide
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.meeple_type import MeepleType
from carcassonne_code2.objects.terrain_type import TerrainType


class MeepleUtil:

    @staticmethod
    def position_contains_meeple(game_state: CarcassonneGameState, coordinate_with_side: CoordinateWithSide) -> Optional[int]:
        for player in range(game_state.players):
            if coordinate_with_side in list(map(lambda x: x.coordinate_with_side, game_state.placed_meeples[player])):
                return player
        return None

    @staticmethod
    def remove_meeples(game_state: CarcassonneGameState, meeples: [[MeeplePosition]]):
        for player, meeple_positions in enumerate(meeples):
            meeple_position: MeeplePosition
            for meeple_position in meeple_positions:
                MeepleUtil.remove_meeple(game_state, meeple_position, player)

    @staticmethod
    def remove_meeple(game_state: CarcassonneGameState, meeple_position: MeeplePosition, player: int):
        game_state.placed_meeples[player].remove(meeple_position)
        if meeple_position.meeple_type == MeepleType.NORMAL or meeple_position.meeple_type == MeepleType.FARMER:
            game_state.meeples[player] += 1
        
    @staticmethod
    def quantity_meeple_on_roads(state: CarcassonneGameState) -> int:
        quantity_placed_road_meeple = 0
        terrrain_type: TerrainType = None
        meeple_position : MeeplePosition
        for meeple_position in state.placed_meeples[state.current_player]:
            terrrain_type = state.board[meeple_position.coordinate_with_side.coordinate.row][
                    meeple_position.coordinate_with_side.coordinate.column].get_type(meeple_position.coordinate_with_side.side)
            if terrrain_type == TerrainType.ROAD:
                quantity_placed_road_meeple += 1
        
        return quantity_placed_road_meeple
    
    @staticmethod
    def quantity_meeple_in_chapels(state: CarcassonneGameState) -> int:
        quantity_placed_chapel_meeple = 0
        terrrain_type: TerrainType = None
        meeple_position : MeeplePosition
        for meeple_position in state.placed_meeples[state.current_player]:
            terrrain_type = state.board[meeple_position.coordinate_with_side.coordinate.row][
                    meeple_position.coordinate_with_side.coordinate.column].get_type(meeple_position.coordinate_with_side.side)
            if terrrain_type == TerrainType.CHAPEL:
                quantity_placed_chapel_meeple += 1
        
        return quantity_placed_chapel_meeple
    
    @staticmethod
    def quantity_meeple_in_cities(state: CarcassonneGameState) -> int:
        quantity_placed_city_meeple = 0
        terrrain_type: TerrainType = None
        meeple_position : MeeplePosition
        for meeple_position in state.placed_meeples[state.current_player]:
            terrrain_type = state.board[meeple_position.coordinate_with_side.coordinate.row][
                    meeple_position.coordinate_with_side.coordinate.column].get_type(meeple_position.coordinate_with_side.side)
            if terrrain_type == TerrainType.CITY:
                quantity_placed_city_meeple += 1
        
        return quantity_placed_city_meeple
    
    @staticmethod
    def quantity_meeple_on_grasses(state: CarcassonneGameState) -> int:
        quantity_placed_grass_meeple = 0
        terrrain_type: TerrainType = None
        meeple_position : MeeplePosition
        for meeple_position in state.placed_meeples[state.current_player]:
            if meeple_position.meeple_type == MeepleType.FARMER:
                quantity_placed_grass_meeple += 1
        
        return quantity_placed_grass_meeple
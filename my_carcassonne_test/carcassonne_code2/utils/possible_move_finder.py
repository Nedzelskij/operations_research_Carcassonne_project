from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.objects.actions.tile_action import TileAction
from carcassonne_code2.objects.coordinate import Coordinate
from carcassonne_code2.objects.actions.meeple_action import MeepleAction
from carcassonne_code2.objects.coordinate_with_side import CoordinateWithSide
from carcassonne_code2.objects.farm import Farm
from carcassonne_code2.objects.farmer_connection import FarmerConnection
from carcassonne_code2.objects.farmer_connection_with_coordinate import FarmerConnectionWithCoordinate
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.meeple_type import MeepleType
from carcassonne_code2.objects.side import Side
from carcassonne_code2.objects.terrain_type import TerrainType
from carcassonne_code2.objects.tile import Tile
from carcassonne_code2.tile_sets.supplementary_rules import SupplementaryRule
from carcassonne_code2.utils.city_util import CityUtil
from carcassonne_code2.utils.farm_util import FarmUtil
from carcassonne_code2.utils.road_util import RoadUtil


class PossibleMoveFinder:

    @classmethod
    def possible_meeple_actions(cls, game_state: CarcassonneGameState) -> [MeepleAction]:
        current_player = game_state.current_player

        possible_actions: [MeepleAction] = []

        meeple_positions = cls.__possible_meeple_positions(game_state=game_state)

        if SupplementaryRule.FARMERS in game_state.supplementary_rules:
            farmer_positions = cls.__possible_farmer_position(game_state=game_state)
        else:
            farmer_positions = ()

        if game_state.meeples[current_player] > 0:
            possible_actions.extend(list(
                map(lambda x: MeepleAction(meeple_type=MeepleType.NORMAL, coordinate_with_side=x), meeple_positions)))

            possible_actions.extend(list(
                map(lambda x: MeepleAction(meeple_type=MeepleType.FARMER, coordinate_with_side=x), farmer_positions)))

        return possible_actions

    @staticmethod
    def __possible_meeple_positions(game_state: CarcassonneGameState) -> [CoordinateWithSide]:
        playing_positions: [CoordinateWithSide] = []
        last_tile_action: TileAction = game_state.last_tile_action
        last_played_tile: Tile = last_tile_action.tile
        last_played_position: Coordinate = last_tile_action.coordinate

        if last_played_tile.chapel:
            playing_positions.append(CoordinateWithSide(coordinate=last_played_position, side=Side.CENTER))

        for side in [Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT]:
            if last_played_tile.get_type(side) == TerrainType.CITY:
                connected_cities = CityUtil.find_city(
                    game_state,
                    CoordinateWithSide(coordinate=last_played_position, side=side)
                )
                if CityUtil.city_contains_meeples(game_state, connected_cities):
                    continue
                else:
                    playing_positions.append(CoordinateWithSide(coordinate=last_played_position, side=side))

            if last_played_tile.get_type(side) == TerrainType.ROAD:
                connected_roads = RoadUtil.find_road(
                    game_state,
                    CoordinateWithSide(coordinate=last_played_position, side=side)
                )
                if RoadUtil.road_contains_meeples(game_state, connected_roads):
                    continue
                else:
                    playing_positions.append(CoordinateWithSide(coordinate=last_played_position, side=side))

        return playing_positions

    @classmethod
    def __possible_farmer_position(cls, game_state: CarcassonneGameState) -> [CoordinateWithSide]:
        playing_positions: [CoordinateWithSide] = []
        last_tile_action: TileAction = game_state.last_tile_action
        last_played_tile: Tile = last_tile_action.tile
        last_played_position: Coordinate = last_tile_action.coordinate

        farmer_connection: FarmerConnection
        for farmer_connection in last_played_tile.farms:
            farm: Farm = FarmUtil.find_farm(
                game_state=game_state,
                farmer_connection_with_coordinate=FarmerConnectionWithCoordinate(farmer_connection, last_played_position)
            )
            if FarmUtil.has_meeples(game_state, farm):
                continue
            else:
                farmer_position: Side = farmer_connection.farmer_positions[0]
                playing_positions.append(CoordinateWithSide(last_played_position, farmer_position))

        return playing_positions
    
    @classmethod
    def check_meeple_actions(cls, state: CarcassonneGameState, meeple_action: tuple) -> bool:
        if not meeple_action:
            return False
        if len(meeple_action) == len('empty'):
            return True

        all_valid_actions: [MeepleAction] = cls.possible_meeple_actions(state)

        valid_action : MeepleAction
        for valid_action in all_valid_actions:
            if valid_action.meeple_type == meeple_action[0] and valid_action.coordinate_with_side.side == meeple_action[1]:
                return True
            
        return False


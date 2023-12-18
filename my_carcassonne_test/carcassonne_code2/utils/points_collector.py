import json
from typing import Set

import numpy as np

from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.objects.city import City
from carcassonne_code2.objects.coordinate import Coordinate
from carcassonne_code2.objects.coordinate_with_side import CoordinateWithSide
from carcassonne_code2.objects.farm import Farm
from carcassonne_code2.objects.farmer_connection_with_coordinate import FarmerConnectionWithCoordinate
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.meeple_type import MeepleType
from carcassonne_code2.objects.road import Road
from carcassonne_code2.objects.side import Side
from carcassonne_code2.objects.terrain_type import TerrainType
from carcassonne_code2.objects.tile import Tile
from carcassonne_code2.utils.city_util import CityUtil
from carcassonne_code2.utils.farm_util import FarmUtil
from carcassonne_code2.utils.meeple_util import MeepleUtil
from carcassonne_code2.utils.road_util import RoadUtil


class PointsCollector:

    @classmethod
    def remove_meeples_and_collect_points(cls, game_state: CarcassonneGameState, coordinate: Coordinate):

        # Points for finished cities
        cities: [City] = CityUtil.find_cities(game_state=game_state, coordinate=coordinate)
        for city in cities:
            if city.finished:
                meeples: [[MeeplePosition]] = CityUtil.find_meeples(game_state=game_state, city=city)
                meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                if sum(meeple_counts_per_player) == 0:
                    continue
                winning_players = cls.get_winning_player(meeple_counts_per_player)
                if winning_players is not None:
                    points = cls.count_city_points(game_state=game_state, city=city)
                    for winning_player in winning_players:
                        game_state.scores[int(winning_player)] += points
                MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples)

        # Points for finished roads
        roads: [Road] = RoadUtil.find_roads(game_state=game_state, coordinate=coordinate)
        for road in roads:
            if road.finished:
                meeples: [[MeeplePosition]] = RoadUtil.find_meeples(game_state=game_state, road=road)
                meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                if sum(meeple_counts_per_player) == 0:
                    continue
                winning_players = cls.get_winning_player(meeple_counts_per_player)
                if winning_players is not None:
                    points = cls.count_road_points(game_state=game_state, road=road)
                    for winning_player in winning_players:
                        game_state.scores[int(winning_player)] += points
                MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples)

        # Points for finished chapels
        for row in range(coordinate.row - 1, coordinate.row + 2):
            for column in range(coordinate.column - 1, coordinate.column + 2):
                tile: Tile = game_state.get_tile(row, column)

                if tile is None:
                    continue

                coordinate = Coordinate(row=row, column=column)
                coordinate_with_side = CoordinateWithSide(coordinate=coordinate, side=Side.CENTER)
                meeple_of_player = MeepleUtil.position_contains_meeple(game_state=game_state,
                                                                             coordinate_with_side=coordinate_with_side)
                if (tile.chapel or tile.flowers) and meeple_of_player is not None:
                    points = cls.chapel_or_flowers_points(game_state=game_state, coordinate=coordinate)
                    if points == 9:
                        game_state.scores[meeple_of_player] += points

                        meeples_per_player = []
                        for _ in range(game_state.players):
                            meeples_per_player.append([])

                        for meeple_position in game_state.placed_meeples[meeple_of_player]:
                            if coordinate_with_side == meeple_position.coordinate_with_side:
                                meeples_per_player[meeple_of_player].append(meeple_position)

                        MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples_per_player)

    @classmethod
    def collect_current_points(cls, game_state: CarcassonneGameState, coordinate: Coordinate) -> dict:
        current_scores: dict = {}
        for player_number in range(len(game_state.placed_meeples)):
            current_scores[player_number] = 0

        # Points for finished cities
        cities: [City] = CityUtil.find_cities(game_state=game_state, coordinate=coordinate)
        for city in cities:
            if city.finished:
                meeples: [[MeeplePosition]] = CityUtil.find_meeples(game_state=game_state, city=city)
                meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                if sum(meeple_counts_per_player) == 0:
                    continue
                winning_players = cls.get_winning_player(meeple_counts_per_player)
                if winning_players is not None:
                    points = cls.count_city_points(game_state=game_state, city=city)
                    for winning_player in winning_players:
                        current_scores[int(winning_player)] += points

        # Points for finished roads
        roads: [Road] = RoadUtil.find_roads(game_state=game_state, coordinate=coordinate)
        for road in roads:
            if road.finished:
                meeples: [[MeeplePosition]] = RoadUtil.find_meeples(game_state=game_state, road=road)
                meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                if sum(meeple_counts_per_player) == 0:
                    continue
                winning_players = cls.get_winning_player(meeple_counts_per_player)
                if winning_players is not None:
                    points = cls.count_road_points(game_state=game_state, road=road)
                    for winning_player in winning_players:
                        current_scores[int(winning_player)] += points

        # Points for finished chapels
        for row in range(coordinate.row - 1, coordinate.row + 2):
            for column in range(coordinate.column - 1, coordinate.column + 2):
                tile: Tile = game_state.get_tile(row, column)

                if tile is None:
                    continue

                coordinate = Coordinate(row=row, column=column)
                coordinate_with_side = CoordinateWithSide(coordinate=coordinate, side=Side.CENTER)
                meeple_of_player = MeepleUtil.position_contains_meeple(game_state=game_state,
                                                                             coordinate_with_side=coordinate_with_side)
                if (tile.chapel or tile.flowers) and meeple_of_player is not None:
                    points = cls.chapel_or_flowers_points(game_state=game_state, coordinate=coordinate)
                    if points == 9:
                        current_scores[meeple_of_player] += points

        return current_scores

    @staticmethod
    def get_winning_player(meeple_counts_per_player: [int]):
        winners = np.argwhere(meeple_counts_per_player == np.amax(meeple_counts_per_player))
        if len(winners) != 0:
            return winners
        else:
            return None

    @staticmethod
    def count_city_points(game_state: CarcassonneGameState, city: City):
        points = 0

        coordinates: Set[Coordinate] = set()
        position: CoordinateWithSide
        for position in city.city_positions:
            coordinate: Coordinate = position.coordinate
            coordinates.add(coordinate)

        tiles: [Tile] = list(map(lambda x: game_state.board[x.row][x.column], coordinates))

        tile: Tile
        for tile in tiles:
            if tile.shield:
                points += 4 if city.finished else 2
            else:
                points += 2 if city.finished else 1

        return points

    @staticmethod
    def count_road_points(game_state: CarcassonneGameState, road: Road):
        points = 0

        coordinates: Set[Coordinate] = set()
        position: CoordinateWithSide
        for position in road.road_positions:
            coordinate: Coordinate = position.coordinate
            coordinates.add(coordinate)

        tiles: [Tile] = list(map(lambda x: game_state.board[x.row][x.column], coordinates))

        tile: Tile
        for _ in tiles:
            points += 1

        return points

    @staticmethod
    def chapel_or_flowers_points(game_state: CarcassonneGameState, coordinate: Coordinate):
        points = 0
        for row in range(coordinate.row - 1, coordinate.row + 2):
            for column in range(coordinate.column - 1, coordinate.column + 2):
                tile: Tile = game_state.board[row][column]
                if tile is not None:
                    points += 1
        return points

    @classmethod
    def count_final_scores(cls, game_state: CarcassonneGameState):
        for player, placed_meeples in enumerate(game_state.placed_meeples):

            # TODO also remove meeples from meeples_to_remove, when there are multiple

            meeples_to_remove: Set[MeeplePosition] = set(placed_meeples)
            while len(meeples_to_remove) > 0:
                meeple_position: MeeplePosition = meeples_to_remove.pop()

                tile: Tile = game_state.board[meeple_position.coordinate_with_side.coordinate.row][
                    meeple_position.coordinate_with_side.coordinate.column]

                terrrain_type: TerrainType = tile.get_type(meeple_position.coordinate_with_side.side)

                if terrrain_type == TerrainType.CITY:
                    city: City = CityUtil.find_city(game_state=game_state,
                                                          city_position=meeple_position.coordinate_with_side)
                    meeples: [CoordinateWithSide] = CityUtil.find_meeples(game_state=game_state, city=city)
                    meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                    winning_players = cls.get_winning_player(meeple_counts_per_player)
                    if winning_players is not None:
                        points = cls.count_city_points(game_state=game_state, city=city)
                        for winning_player in winning_players:
                            game_state.scores[int(winning_player)] += points

                    MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples)
                    continue

                if terrrain_type == TerrainType.ROAD:
                    road: [Road] = RoadUtil.find_road(game_state=game_state,
                                                            road_position=meeple_position.coordinate_with_side)
                    meeples: [CoordinateWithSide] = RoadUtil.find_meeples(game_state=game_state, road=road)
                    meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                    winning_players = cls.get_winning_player(meeple_counts_per_player)
                    if winning_players is not None:
                        points = cls.count_road_points(game_state=game_state, road=road)
                        for winning_player in winning_players:
                            game_state.scores[int(winning_player)] += points
                    MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples)
                    continue

                if terrrain_type == TerrainType.CHAPEL or terrrain_type == TerrainType.FLOWERS:
                    points = cls.chapel_or_flowers_points(game_state=game_state,
                                                           coordinate=meeple_position.coordinate_with_side.coordinate)
                    game_state.scores[player] += points

                    meeples_per_player = []
                    for _ in range(game_state.players):
                        meeples_per_player.append([])
                    meeples_per_player[player].append(meeple_position)

                    MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples_per_player)
                    continue

                if meeple_position.meeple_type == MeepleType.FARMER:
                    farm: Farm = FarmUtil.find_farm_by_coordinate(game_state=game_state, position=meeple_position.coordinate_with_side)
                    meeples: [[MeeplePosition]] = FarmUtil.find_meeples(game_state=game_state, farm=farm)
                    meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                    winning_players = cls.get_winning_player(meeple_counts_per_player)
                    if winning_players is not None:
                        points = cls.count_farm_points(game_state=game_state, farm=farm)
                        for winning_player in winning_players:
                            game_state.scores[int(winning_player)] += points
                    MeepleUtil.remove_meeples(game_state=game_state, meeples=meeples)
                    continue

    @classmethod
    def count_current_final_scores(cls, game_state: CarcassonneGameState) -> dict:
        current_final_scores: dict = {}
        for player_number in range(len(game_state.placed_meeples)):
            current_final_scores[player_number] = 0

        for player, placed_meeples in enumerate(game_state.placed_meeples):

            meeples_to_remove: Set[MeeplePosition] = set(placed_meeples)
            while len(meeples_to_remove) > 0:
                meeple_position: MeeplePosition = meeples_to_remove.pop()

                tile: Tile = game_state.board[meeple_position.coordinate_with_side.coordinate.row][
                    meeple_position.coordinate_with_side.coordinate.column]

                terrrain_type: TerrainType = tile.get_type(meeple_position.coordinate_with_side.side)

                if terrrain_type == TerrainType.CITY:
                    city: City = CityUtil.find_city(game_state=game_state,
                                                          city_position=meeple_position.coordinate_with_side)
                    if not city.finished:
                        meeples: [CoordinateWithSide] = CityUtil.find_meeples(game_state=game_state, city=city)
                        meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                        winning_players = cls.get_winning_player(meeple_counts_per_player)
                        divide_index = max(meeple_counts_per_player)
                        if winning_players is not None:
                            points = cls.count_city_points(game_state=game_state, city=city)
                            for winning_player in winning_players:
                                if int(winning_player) == player:
                                    current_final_scores[player] += points / divide_index
                    continue

                if terrrain_type == TerrainType.ROAD:
                    road: [Road] = RoadUtil.find_road(game_state=game_state,
                                                            road_position=meeple_position.coordinate_with_side)
                    if not road.finished:
                        meeples: [CoordinateWithSide] = RoadUtil.find_meeples(game_state=game_state, road=road)
                        meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                        winning_players = cls.get_winning_player(meeple_counts_per_player)
                        divide_index = max(meeple_counts_per_player)
                        if winning_players is not None:
                            points = cls.count_road_points(game_state=game_state, road=road)
                            for winning_player in winning_players:
                                if int(winning_player) == player:
                                    current_final_scores[player] += points / divide_index
                    continue

                if terrrain_type == TerrainType.CHAPEL or terrrain_type == TerrainType.FLOWERS:
                    points = cls.chapel_or_flowers_points(game_state=game_state,
                                                           coordinate=meeple_position.coordinate_with_side.coordinate)
                    if points != 9:
                        current_final_scores[player] += points
                    continue
                    
                if meeple_position.meeple_type == MeepleType.FARMER:
                    farm: Farm = FarmUtil.find_farm_by_coordinate(game_state=game_state, position=meeple_position.coordinate_with_side)
                    meeples: [[MeeplePosition]] = FarmUtil.find_meeples(game_state=game_state, farm=farm)
                    meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                    winning_players = cls.get_winning_player(meeple_counts_per_player)
                    divide_index = max(meeple_counts_per_player)
                    if winning_players is not None:
                        points = cls.count_farm_points(game_state=game_state, farm=farm)
                        for winning_player in winning_players:
                            if int(winning_player) == player:
                                current_final_scores[player] += points / divide_index
                    continue

        return current_final_scores

    @classmethod
    def count_current_final_meeple_scores(cls, game_state: CarcassonneGameState, meeple_position: MeeplePosition) -> int:
        final_points = 0

        tile: Tile = game_state.board[meeple_position.coordinate_with_side.coordinate.row][
            meeple_position.coordinate_with_side.coordinate.column]

        terrrain_type: TerrainType = tile.get_type(meeple_position.coordinate_with_side.side)

        if terrrain_type == TerrainType.CITY:
            city: City = CityUtil.find_city(game_state=game_state,
                                                    city_position=meeple_position.coordinate_with_side)
            if not city.finished:
                meeples: [CoordinateWithSide] = CityUtil.find_meeples(game_state=game_state, city=city)
                meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                winning_players = cls.get_winning_player(meeple_counts_per_player)
                if winning_players is not None:
                    points = cls.count_city_points(game_state=game_state, city=city)
                    final_points += points

        if terrrain_type == TerrainType.ROAD:
            road: [Road] = RoadUtil.find_road(game_state=game_state,
                                                    road_position=meeple_position.coordinate_with_side)
            if not road.finished:
                meeples: [CoordinateWithSide] = RoadUtil.find_meeples(game_state=game_state, road=road)
                meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
                winning_players = cls.get_winning_player(meeple_counts_per_player)
                if winning_players is not None:
                    points = cls.count_road_points(game_state=game_state, road=road)
                    final_points += points

        if terrrain_type == TerrainType.CHAPEL or terrrain_type == TerrainType.FLOWERS:
            points = cls.chapel_or_flowers_points(game_state=game_state,
                                                    coordinate=meeple_position.coordinate_with_side.coordinate)
            if points != 9:
                final_points += points

        if meeple_position.meeple_type == MeepleType.FARMER: # or meeple_position.meeple_type == MeepleType.BIG_FARMER:
            farm: Farm = FarmUtil.find_farm_by_coordinate(game_state=game_state, position=meeple_position.coordinate_with_side)
            meeples: [[MeeplePosition]] = FarmUtil.find_meeples(game_state=game_state, farm=farm)
            meeple_counts_per_player = cls.get_meeple_counts_per_player(meeples)
            winning_players = cls.get_winning_player(meeple_counts_per_player)
            if winning_players is not None:
                points = cls.count_farm_points(game_state=game_state, farm=farm)
                final_points += points
                   
        return final_points
            

    @staticmethod
    def get_meeple_counts_per_player(meeples: [[MeeplePosition]]):
        meeple_counts_per_player = list(
            map(
                lambda x:
                sum(list(map(
                    lambda y: 2 if y.meeple_type == MeepleType.BIG or y.meeple_type == MeepleType.BIG_FARMER else 1, x
                ))),
                meeples
            )
        )
        return meeple_counts_per_player

    @classmethod
    def count_farm_points(cls, game_state: CarcassonneGameState, farm: Farm):
        cities: Set[City] = set()
        finished_cities: [City] = []
        point_index = False

        points = 0
        
        farmer_connection_with_coordinate: FarmerConnectionWithCoordinate
        for farmer_connection_with_coordinate in farm.farmer_connections_with_coordinate:
            cities = cities.union(CityUtil.find_cities(game_state=game_state, coordinate=farmer_connection_with_coordinate.coordinate, sides=farmer_connection_with_coordinate.farmer_connection.city_sides))

        city: City
        for city in cities:
            if city.finished:
                finished_cities.append(city)
                
        while finished_cities:
            poped_city: City = finished_cities.pop()
            point_index = True
            if not finished_cities:
                points += 3
                continue
            
            for finished_city in finished_cities:
                if len(finished_city.city_positions) == len([x for x in finished_city.city_positions if x in poped_city.city_positions]) and \
                        len(poped_city.city_positions) == len([x for x in poped_city.city_positions if x in finished_city.city_positions]) and finished_city.finished == poped_city.finished:
                    point_index = False
                    break
            
            if point_index:
                points += 3

        return points

from typing import Set

from carcassonne_code2.carcassonne_game_state import CarcassonneGameState
from carcassonne_code2.objects.city import City
from carcassonne_code2.objects.coordinate import Coordinate
from carcassonne_code2.objects.coordinate_with_side import CoordinateWithSide
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.side import Side
from carcassonne_code2.objects.terrain_type import TerrainType
from carcassonne_code2.objects.tile import Tile


class CityUtil:

    @classmethod
    def find_city(cls, game_state: CarcassonneGameState, city_position: CoordinateWithSide) -> City:
        cities: Set[CoordinateWithSide] = set(cls.cities_for_position(game_state, city_position))
        open_edges: Set[CoordinateWithSide] = set(map(lambda x: cls.opposite_edge(x), cities))
        explored: Set[CoordinateWithSide] = cities.union(open_edges)

        while len(open_edges) > 0:
            open_edge: CoordinateWithSide = open_edges.pop()
            new_cities = cls.cities_for_position(game_state, open_edge)
            cities = cities.union(new_cities)
            new_open_edges = set(map(lambda x: cls.opposite_edge(x), new_cities))
            explored = explored.union(new_cities)
            
            new_open_edge: CoordinateWithSide
            for new_open_edge in new_open_edges: 
                if new_open_edge not in explored:
                    open_edges.add(new_open_edge)
                    explored.add(new_open_edge)

        finished: bool = len(explored) == len(cities)
        return City(city_positions=cities, finished=finished)
    
    @classmethod
    def find_quantity_empty_city_sides(cls, game_state: CarcassonneGameState, city_position: CoordinateWithSide) -> int:
        cities: Set[CoordinateWithSide] = set(cls.cities_for_position(game_state, city_position))
        open_edges: Set[CoordinateWithSide] = set(map(lambda x: cls.opposite_edge(x), cities))
        explored: Set[CoordinateWithSide] = cities.union(open_edges)

        while len(open_edges) > 0:
            open_edge: CoordinateWithSide = open_edges.pop()
            new_cities = cls.cities_for_position(game_state, open_edge)
            cities = cities.union(new_cities)
            new_open_edges = set(map(lambda x: cls.opposite_edge(x), new_cities))
            explored = explored.union(new_cities)
            
            new_open_edge: CoordinateWithSide
            for new_open_edge in new_open_edges: 
                if new_open_edge not in explored:
                    open_edges.add(new_open_edge)
                    explored.add(new_open_edge)

        quantity_empty_sides: int = len(explored) - len(cities)
        return quantity_empty_sides

    @classmethod
    def opposite_edge(cls, city_position: CoordinateWithSide):
        if city_position.side == Side.TOP:
            return CoordinateWithSide(Coordinate(city_position.coordinate.row - 1, city_position.coordinate.column),
                                      Side.BOTTOM)
        elif city_position.side == Side.RIGHT:
            return CoordinateWithSide(Coordinate(city_position.coordinate.row, city_position.coordinate.column + 1),
                                      Side.LEFT)
        elif city_position.side == Side.BOTTOM:
            return CoordinateWithSide(Coordinate(city_position.coordinate.row + 1, city_position.coordinate.column),
                                      Side.TOP)
        elif city_position.side == Side.LEFT:
            return CoordinateWithSide(Coordinate(city_position.coordinate.row, city_position.coordinate.column - 1),
                                      Side.RIGHT)

    @classmethod
    def cities_for_position(cls, game_state: CarcassonneGameState, city_position: CoordinateWithSide):
        tile: Tile = game_state.board[city_position.coordinate.row][city_position.coordinate.column]
        cities = []
        if tile is None:
            return cities
        for city_group in tile.city:
            if city_position.side in city_group:
                city_group_side: Side
                for city_group_side in city_group:
                    city_position: CoordinateWithSide = CoordinateWithSide(city_position.coordinate, city_group_side)
                    cities.append(city_position)
        return cities

    @classmethod
    def city_contains_meeples(cls, game_state: CarcassonneGameState, city: City):
        for city_position in city.city_positions:
            for i in range(game_state.players):
                if city_position in list(map(lambda x: x.coordinate_with_side, game_state.placed_meeples[i])):
                    return True
        return False

    @classmethod
    def find_meeples(cls, game_state: CarcassonneGameState, city: City) -> [[MeeplePosition]]:
        meeples: [[MeeplePosition]] = []

        for i in range(game_state.players):
            meeples.append([])

        for city_position in city.city_positions:
            for i in range(game_state.players):
                meeple_position: MeeplePosition
                for meeple_position in game_state.placed_meeples[i]:
                    if city_position == meeple_position.coordinate_with_side:
                        meeples[i].append(meeple_position)

        return meeples
    
    @classmethod
    def find_cities(cls, game_state: CarcassonneGameState, coordinate: Coordinate, sides: [Side] = (Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT)):
        cities: Set[City] = set()
        list_cities: [City] = []
        unique_cities: [City] = []
        city_index = False

        tile: Tile = game_state.board[coordinate.row][coordinate.column]

        if tile is None:
            return cities

        side: Side
        for side in sides:
            if tile.get_type(side) == TerrainType.CITY:
                city: City = cls.find_city(game_state=game_state,
                                            city_position=CoordinateWithSide(coordinate=coordinate, side=side))
                cities.add(city)

        list_cities = list(cities)

        while list_cities:
            poped_city: City = list_cities.pop()
            city_index = True
            if not list_cities:
                unique_cities.append(poped_city)
                continue
            
            list_city: City
            for list_city in list_cities:
                if len(list_city.city_positions) == len([x for x in list_city.city_positions if x in poped_city.city_positions]) and \
                        len(poped_city.city_positions) == len([x for x in poped_city.city_positions if x in list_city.city_positions]) and list_city.finished == poped_city.finished:
                    city_index = False
                    break
            
            if city_index:
                unique_cities.append(poped_city)
            
        return unique_cities
    
    @classmethod
    def find_quantity_empty_cities_sides(cls, game_state: CarcassonneGameState, coordinate: Coordinate, sides: [Side] = (Side.TOP, Side.RIGHT, Side.BOTTOM, Side.LEFT)):
        empty_cities_sides: [int] = [0]

        tile: Tile = game_state.board[coordinate.row][coordinate.column]

        if tile is None:
            return empty_cities_sides

        side: Side
        for side in sides:
            if tile.get_type(side) == TerrainType.CITY:
                empty_cities_side: int = cls.find_quantity_empty_city_sides(game_state=game_state,
                                            city_position=CoordinateWithSide(coordinate=coordinate, side=side))
                empty_cities_sides.append(empty_cities_side)

        return max(empty_cities_sides)

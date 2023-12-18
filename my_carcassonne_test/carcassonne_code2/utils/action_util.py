from carcassonne_code2.carcassonne_game_state import CarcassonneGameState, GamePhase
from carcassonne_code2.objects.actions.action import Action
from carcassonne_code2.objects.actions.pass_action import PassAction
from carcassonne_code2.objects.actions.tile_action import TileAction
from carcassonne_code2.objects.actions.meeple_action import MeepleAction
from carcassonne_code2.objects.meeple_position import MeeplePosition
from carcassonne_code2.objects.playing_position import PlayingPosition
from carcassonne_code2.utils.possible_move_finder import PossibleMoveFinder
from carcassonne_code2.utils.tile_position_finder import TilePositionFinder
from carcassonne_code2.objects.coordinate import Coordinate
from carcassonne_code2.objects.coordinate_with_side import CoordinateWithSide
from carcassonne_code2.utils.points_collector import PointsCollector
from carcassonne_code2.utils.state_updater import StateUpdater
from carcassonne_code2.objects.terrain_type import TerrainType
from carcassonne_code2.utils.city_util import CityUtil
from carcassonne_code2.utils.meeple_util import MeepleUtil

class ActionUtil:

    @staticmethod
    def get_possible_actions(state: CarcassonneGameState):
        actions: [Action] = []
        if state.phase == GamePhase.TILES:
            possible_playing_positions: [PlayingPosition] = TilePositionFinder.possible_playing_positions(
                game_state=state,
                tile_to_play=state.next_tile
            )
            if len(possible_playing_positions) == 0:
                actions.append(PassAction())
            else:
                playing_position: PlayingPosition
                for playing_position in possible_playing_positions:
                    action = TileAction(
                        tile=state.next_tile.turn(playing_position.turns),
                        coordinate=playing_position.coordinate,
                        tile_rotations=playing_position.turns
                    )
                    actions.append(action)
        elif state.phase == GamePhase.MEEPLES:
            possible_meeple_actions = PossibleMoveFinder.possible_meeple_actions(game_state=state)
            actions.extend(possible_meeple_actions)
            actions.append(PassAction())
        return actions
    
    @staticmethod
    def get_possible_tile_actions(state: CarcassonneGameState):
        actions: [Action] = []
        possible_playing_positions: [PlayingPosition] = TilePositionFinder.possible_playing_positions(
                game_state=state,
                tile_to_play=state.next_tile
            )
        if len(possible_playing_positions) == 0:
            # actions.append(PassAction())
            pass
        else:
            playing_position: PlayingPosition
            for playing_position in possible_playing_positions:
                action = TileAction(
                    tile=state.next_tile.turn(playing_position.turns),
                    coordinate=playing_position.coordinate,
                    tile_rotations=playing_position.turns
                )
                actions.append(action)
        return actions
    
    @staticmethod
    def get_possible_meeple_actions(state: CarcassonneGameState):
        actions: [Action] = []
        possible_meeple_actions = PossibleMoveFinder.possible_meeple_actions(game_state=state)
        actions.extend(possible_meeple_actions)
        actions.append(PassAction())
        return actions
    
    @staticmethod
    def get_initial_tile(state: CarcassonneGameState) -> Action:
        playing_position: PlayingPosition = PlayingPosition(coordinate=state.starting_position, turns=0)
        action = TileAction(
                        tile=state.next_tile.turn(playing_position.turns),
                        coordinate=playing_position.coordinate,
                        tile_rotations=playing_position.turns
                    )
        return action

    @staticmethod
    def get_tile_action(state: CarcassonneGameState, row_index: int, column_index: int, tile_turns: int) -> Action:
        playing_position = PlayingPosition(coordinate=Coordinate(row=row_index, column=column_index), turns=tile_turns)
            
        return TileAction(
                        tile=state.next_tile.turn(playing_position.turns),
                        coordinate=playing_position.coordinate,
                        tile_rotations=playing_position.turns
                    )
    
    @staticmethod
    def get_meeple_action(state: CarcassonneGameState, meeple_action : tuple) -> Action:
        last_played_position: Coordinate = state.last_tile_action.coordinate

        if len(meeple_action) == len('empty'):
            return PassAction()
        
        return MeepleAction(meeple_type=meeple_action[0], coordinate_with_side=CoordinateWithSide(last_played_position, meeple_action[1]))

    @classmethod
    def set_optimal_tile_meeple_action(cls, state: CarcassonneGameState):
        final_points_before_tile_action: dict = {}
        final_points_after_tile_action: dict = {}
        computer_final_points_after_tile_action = 0
        opponent_final_points_after_tile_action = 0
        points_after_tile_action: dict = {}
        computer_points_after_tile_action = 0
        opponent_points_after_tile_action = 0
        meeple_points_action: dict = {}
        computer_meeple_points_action = 0
        computer_final_meeple_points_action = 0
        pass_action = False
        terrain_type: TerrainType = None
        empty_city_sides = 0
        
        final_points_before_tile_action = PointsCollector.count_current_final_scores(state)
        
        tile_actions: [TileAction] = cls.get_possible_tile_actions(state)
        if len(tile_actions) == 0:
            state.next_tile = state.deck.pop(0)
            cls.set_optimal_tile_meeple_action(state)

        tile_action: TileAction
        for tile_action in tile_actions:
            StateUpdater.play_current_tile(game_state=state, tile_action=tile_action)
            final_points_after_tile_action = PointsCollector.count_current_final_scores(state)
            for key, value in final_points_after_tile_action.items():
                if key == state.current_player:
                    computer_final_points_after_tile_action = value - final_points_before_tile_action[key]
                else:
                    if (value - final_points_before_tile_action[key]) > opponent_final_points_after_tile_action:
                        opponent_final_points_after_tile_action = value - final_points_before_tile_action[key]
            
            points_after_tile_action = PointsCollector.collect_current_points(game_state=state, coordinate=tile_action.coordinate)
            for key, value in points_after_tile_action.items():
                if key == state.current_player:
                    computer_points_after_tile_action = value
                else:
                    if value > opponent_points_after_tile_action:
                        opponent_points_after_tile_action = value

            empty_city_sides = CityUtil.find_quantity_empty_cities_sides(game_state=state, coordinate=tile_action.coordinate)

            meeple_actions: [MeepleAction] = cls.get_possible_meeple_actions(state) 
            meeple_action: MeepleAction
            for meeple_action in meeple_actions:
                if isinstance(meeple_action, PassAction):
                    pass_action = True
                else:
                    StateUpdater.play_current_meeple(game_state=state, meeple_action=meeple_action)
                    meeple_points_action = PointsCollector.collect_current_points(game_state=state, coordinate=tile_action.coordinate)
                    computer_meeple_points_action = meeple_points_action[state.current_player] - computer_points_after_tile_action

                    current_meeple_position: MeeplePosition = state.placed_meeples[state.current_player].pop()
                    computer_final_meeple_points_action = PointsCollector.count_current_final_meeple_scores(game_state=state, meeple_position=current_meeple_position)
                    
                    terrain_type: TerrainType = tile_action.tile.get_type(current_meeple_position.coordinate_with_side.side)

                current_priority = cls.set_priority(state, terrain_type, computer_final_points_after_tile_action, opponent_final_points_after_tile_action,
                                                    computer_points_after_tile_action, opponent_points_after_tile_action,
                                                    computer_final_meeple_points_action, computer_meeple_points_action, pass_action, empty_city_sides)

                if current_priority > state.computer_action_priority:
                    state.computer_action_priority = current_priority
                    state.final_computer_tile_action = tile_action
                    state.final_computer_meeple_action = meeple_action
                    
                terrain_type = None
                computer_meeple_points_action = 0
                computer_final_meeple_points_action = 0
                pass_action = False

            computer_points_after_tile_action = 0
            opponent_points_after_tile_action = 0
            opponent_final_points_after_tile_action = 0
            computer_final_points_after_tile_action = 0
            StateUpdater.clear_current_tile_action(game_state=state, tile_action=tile_action)

    @staticmethod
    def set_priority(state: CarcassonneGameState, terrain_type: TerrainType, comp_T_f_p, opponent_T_f_p,
                      comp_i_p, opponent_i_p, mepple_f_p, mepple_i_p, pass_action, quantity_empty_city_sides) -> float:
        k_1, k_2, k_3 = - 10, - 1.6, 1.2
        k_4, k_5, k_6 = 8, 10, 1
        pass_p = 1
        priority: float = 0
        meeple_quantity = state.meeples[state.current_player]
        tile_quantity = len(state.deck)

        if comp_i_p > 0 or mepple_i_p > 0:
            meeple_quantity += 1

        if pass_action:
            if quantity_empty_city_sides > 0:
                k_3 = 1.4

            if quantity_empty_city_sides > 3:
                k_3 = -1
            elif quantity_empty_city_sides > 2 and tile_quantity < 30:
                k_3 = -1

            priority = k_1 * opponent_i_p + k_2 * opponent_T_f_p + k_3 * comp_T_f_p + \
                       k_4 * comp_i_p + pass_p
        else:
            if terrain_type == TerrainType.ROAD:
                if meeple_quantity <= 2 or MeepleUtil.quantity_meeple_on_roads(state) > 1:
                    k_6 = 0

                if quantity_empty_city_sides > 3:
                    k_3 = -1.1
                elif quantity_empty_city_sides > 2 and tile_quantity < 30:
                    k_3 = -1.1
            elif terrain_type == TerrainType.CITY:
                k_6 = 1.3
                if meeple_quantity <= 1:
                    k_6 = 0

                if MeepleUtil.quantity_meeple_in_cities(state) > 2:
                    k_6 = 0

                if quantity_empty_city_sides > 3:
                    k_6 = -1
                elif quantity_empty_city_sides > 2 and tile_quantity < 30:
                    k_6 = -1

                if tile_quantity <= 5:
                    k_6 = 1
            elif terrain_type == TerrainType.CHAPEL:

                if meeple_quantity >= 3:
                    k_6 = 1.5
                elif meeple_quantity <= 1:
                    k_6 = 0

                if MeepleUtil.quantity_meeple_in_chapels(state) > 1:
                    k_6 = 0

                if tile_quantity <= 10:
                    k_6 = 1  
            else: # terrain_type == TerrainType.GRASS:
                k_6 = 0
                if mepple_f_p >= 9 and meeple_quantity > 1:
                    k_6 = 1
                elif mepple_f_p >= 6 and meeple_quantity > 1 and (tile_quantity > 50 or tile_quantity < 20) \
                     and MeepleUtil.quantity_meeple_on_grasses(state) < 1:
                    k_6 = 1

                if quantity_empty_city_sides > 3:
                    k_3 = -1
                elif quantity_empty_city_sides > 2 and tile_quantity < 30:
                    k_3 = -1

                if tile_quantity <= 10:
                    k_6 = 1

            priority = k_1 * opponent_i_p + k_2 * opponent_T_f_p + k_3 * comp_T_f_p + \
                    k_4 * comp_i_p + k_5 * mepple_i_p + k_6 * mepple_f_p

        return priority     

    @classmethod
    def get_computer_tile_meeple_action(cls, state: CarcassonneGameState):
        if state.computer_action_priority == -100:
            cls.set_optimal_tile_meeple_action(state)

        if state.phase == GamePhase.TILES:
            return state.final_computer_tile_action
        elif state.phase == GamePhase.MEEPLES:
            state.computer_action_priority = -100
            return state.final_computer_meeple_action

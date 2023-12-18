import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

import carcassonne_code2.carcassonne_representer as visualiser
from carcassonne_code2.carcassonne_play import CarcassonnePlay
from carcassonne_code2.carcassonne_game_state import CarcassonneGameState, GamePhase
from carcassonne_code2.objects.actions.action import Action
from carcassonne_code2.objects.meeple_type import MeepleType
from carcassonne_code2.tile_sets.supplementary_rules import SupplementaryRule
from carcassonne_code2.tile_sets.tile_sets import TileSet


def clear_player_tile_chice_xy():
    visualiser.x_mouse_coords, visualiser.y_mouse_coords = -1000, -1000

def clear_player_meeple_choice():
    visualiser.meeple_tipe_action = ()


game = CarcassonnePlay(
    players=2,
    tile_sets=[TileSet.BASE, TileSet.THE_RIVER], 
    supplementary_rules=[SupplementaryRule.FARMERS]
)

game.set_initial_tile()

while not game.is_finished():
    player: int = game.get_current_player()
    
    if player == 1:
        if game.state.phase == GamePhase.TILES:
            clear_player_tile_chice_xy()
            while not game.check_player_tile_action(game.state.next_tile, int((visualiser.y_mouse_coords + visualiser.canvas_height_change)/ 60), 
                                            int((visualiser.x_mouse_coords + visualiser.canvas_width_change) / 60), visualiser.next_tile_turns):
                clear_player_tile_chice_xy()
                game.render()
        
            action: Action = game.get_player_tile_action(int((visualiser.y_mouse_coords + visualiser.canvas_height_change)/ 60), 
                                            int((visualiser.x_mouse_coords + visualiser.canvas_width_change) / 60), visualiser.next_tile_turns)
        else: # GamePhase.MEEPLE
            clear_player_meeple_choice()
            while not game.check_player_meeple_action(visualiser.meeple_tipe_action):
                game.render()
            
            action : Action = game.get_player_meeple_action(visualiser.meeple_tipe_action)
    else:
        action : Action = game.get_computer_action()
    
    if action is not None: 
        game.step(player, action)
    game.render()

input("Press Enter to continue...")
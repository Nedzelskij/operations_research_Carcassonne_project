from carcassonne_code2.objects.actions.action import Action
from carcassonne_code2.objects.coordinate_with_side import CoordinateWithSide
from carcassonne_code2.objects.meeple_type import MeepleType


class MeepleAction(Action):
    def __init__(self, meeple_type: MeepleType, coordinate_with_side: CoordinateWithSide, remove: bool = False):
        self.meeple_type = meeple_type
        self.coordinate_with_side = coordinate_with_side
        self.remove = remove
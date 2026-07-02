from config import CONFIG
from entities.entity import Entity


class Plant(Entity):
    t_plant = CONFIG["T_plant"]
    SIGN = "🍀"

    def __init__(self, row, col):
        Entity.__init__(self, row, col)


    def step(self, board: list):
        """Implements plant functionality."""
        self.increase_age()
        if self.is_dead(Plant.t_plant):
            self.remove_from_board(board)

from entities.entity import Entity


class Plant(Entity):
    t_plant = 0
    SIGN = "🍀"

    def __init__(self, row, col):
        Entity.__init__(self, row, col)

    def print_entity(self):
        print(Plant.SIGN, end="")

    def step(self, board: list):
        """Implements plant functionality."""
        self.increase_age()
        if self.is_dead(Plant.t_plant):
            self.remove_from_board(board)

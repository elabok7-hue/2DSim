import random
from entities.herbivore import Herbivore
from entities.plant import Plant


class Predator:
    t_predator = 10
    r_predator_sight = 2
    t_cooldown = 10

    def __init__(self, row, col):
        self.age = 0
        self.row = row
        self.col = col

    def increase_age(self):
        self.age += 1

    def find_nearest_herbivore(self, board: list):
        """Finds the nearest herbivore within sight radius."""
        for sight in range(1, self.r_predator_sight + 1):
            for check_row in range(self.row - sight, self.row + sight + 1):
                if 0 <= check_row < len(board):
                    for check_col in range(self.col - sight, self.col + sight + 1):
                        if 0 <= check_col < len(board[check_row]):
                            entity = board[check_row][check_col]

                            if isinstance(entity, Herbivore):
                                return entity
                                
        return None

    def move_towards_herbivore(self, herbivore: Herbivore):
        if herbivore.row > self.row:
            self.row += 1
        elif herbivore.row < self.row:
            self.row -= 1
        if herbivore.col > self.col:
            self.col += 1
        elif herbivore.col < self.col:
            self.col -= 1

    def is_dead(self):
        return self.age >= self.t_predator

    def refuel_life_span(self):
        self.age = 0

    def move_randomly(self, board: list):
        """Move to a random neighboring cell."""
        rows = len(board)
        cols = len(board[0])
        new_row = random.randrange(max(0, self.row - 1), min(rows, self.row + 2))
        new_col = random.randrange(max(0, self.col - 1), min(cols, self.col + 2))
        self.row = new_row
        self.col = new_col

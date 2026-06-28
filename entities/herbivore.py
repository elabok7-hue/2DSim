import random
from entities.mobile_entity import MobileEntity


class Herbivore(MobileEntity):
    t_herbivore = 10
    r_herbivore_sight = 2
    t_cooldown = 6

    def __init__(self, row, col):
        MobileEntity.__init__(self, row, col)

        self.reproduction_cooldown_timer = 0

    def can_reproduce(self):
        return self.reproduction_cooldown_timer == 0

    def reproduce(self, board: list):
        """Try to spawn a new herbivore in a random empty neighboring cell."""
        self.reproduction_cooldown_timer = self.t_cooldown
        rows = len(board)
        cols = len(board[0])

        empty_cells = []
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = self.row + dr, self.col + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] is None:
                    empty_cells.append((nr, nc))

        if empty_cells:
            nr, nc = random.choice(empty_cells)
            baby = Herbivore(nr, nc)
            return baby

        return None

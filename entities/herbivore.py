import random
from entities.plant import Plant


class Herbivore:
    t_herbivore = 10
    r_herbivore_sight = 2
    t_cooldown = 6

    def __init__(self, row, col):
        self.age = 0
        self.row = row
        self.col = col
        self.cooldown_timer = 0  # tracks reproduction cooldown

    def increase_age(self):
        self.age += 1
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def find_nearest_plant(self, board: list):
        """Finds the nearest plant within sight radius."""
        for sight in range(1, self.r_herbivore_sight + 1):
            for check_row in range(self.row - sight, self.row + sight + 1):
                if 0 <= check_row < len(board):
                    for check_col in range(self.col - sight, self.col + sight + 1):
                        if 0 <= check_col < len(board[check_row]):
                            entity = board[check_row][check_col]

                            if isinstance(entity, Plant):
                                return entity

        return None

    def find_nearest_herbivore(self, board: list):
        """Finds the nearest other herbivore within sight radius (for reproduction)."""
        for sight in range(1, self.r_herbivore_sight + 1):
            for check_row in range(self.row - sight, self.row + sight + 1):
                if 0 <= check_row < len(board):
                    for check_col in range(self.col - sight, self.col + sight + 1):
                        if 0 <= check_col < len(board[check_row]):
                            entity = board[check_row][check_col]
                            if isinstance(entity, Herbivore) and entity is not self:
                                return entity

        return None

    def is_dead(self):
        return self.age >= self.t_herbivore

    def move_towards(self, target):
        """Move one step towards a target entity (plant or herbivore)."""
        if target.row > self.row:
            self.row += 1
        elif target.row < self.row:
            self.row -= 1
        if target.col > self.col:
            self.col += 1
        elif target.col < self.col:
            self.col -= 1

    def move_towards_plant(self, plant: Plant):
        """Kept for backwards compatibility — calls move_towards."""
        self.move_towards(plant)

    def move_randomly(self, board: list):
        """Move to a random neighboring cell, clamped to board bounds."""
        rows = len(board)
        cols = len(board[0])
        new_row = random.randrange(max(0, self.row - 1), min(rows, self.row + 2))
        new_col = random.randrange(max(0, self.col - 1), min(cols, self.col + 2))
        self.row = new_row
        self.col = new_col

    def refuel_life_span(self):
        self.age = 0

    def can_reproduce(self):
        return self.cooldown_timer == 0

    def reproduce(self, board: list):
        """Try to spawn a new herbivore in a random empty neighboring cell."""
        self.cooldown_timer = self.t_cooldown
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

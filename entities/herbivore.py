import random

from entities import Plant
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

    def herbivore_step(self, board: list):
        """Implements herbivore functionality."""
        self.increase_age()

        if self.is_dead(Herbivore.t_herbivore):
            self.remove_from_board(board)
        else:

            old_row, old_col = self.row, self.col

            if self.can_reproduce():
                partner = self.find_nearest_needed_entity(board, Herbivore, 1)

                if partner is not None:
                    baby = self.reproduce(board)

                    if baby:
                        board[baby.row][baby.col] = baby

                    self.cooldown_timer = self.t_cooldown
                    partner.cooldown_timer = partner.t_cooldown
                    return

            nearest_plant = self.find_nearest_needed_entity(board, Plant, Herbivore.r_herbivore_sight)
            if nearest_plant is None:
                self.move_randomly(board)
            else:
                self.move_towards_entity(nearest_plant)

            self.move_entity_on_board(old_row, old_col, board)
            target = board[self.row][self.col]

            if isinstance(target, Plant) and target is not self:
                target.remove_from_board(board)
                self.refuel_life_span()
            board[self.row][self.col] = self


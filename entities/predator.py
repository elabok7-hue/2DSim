from entities import Herbivore, Plant
from entities.mobile_entity import MobileEntity


class Predator(MobileEntity):
    t_predator = 10
    r_predator_sight = 2
    t_cooldown = 10

    def __init__(self, row, col):
        MobileEntity.__init__(self, row, col)

    def predator_step(self, board: list):
        """Implements predator functionality."""
        self.increase_age()

        if self.is_dead(Predator.t_predator):
            self.remove_from_board(board)
        else:

            old_row, old_col = self.row, self.col

            nearest_herbivore = self.find_nearest_needed_entity(board, Herbivore, Herbivore.r_herbivore_sight)
            if nearest_herbivore is None:
                self.move_randomly(board)
            else:
                self.move_towards_entity(nearest_herbivore)

            self.move_entity_on_board(old_row, old_col, board)

            target = board[self.row][self.col]

            if isinstance(target, Herbivore):
                target.remove_from_board(board)
                self.refuel_life_span()
            elif isinstance(target, Plant):
                target.remove_from_board(board)

            board[self.row][self.col] = self


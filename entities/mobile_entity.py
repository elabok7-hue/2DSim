import random

from entities.entity import Entity


class MobileEntity(Entity):

    def __init__(self, row, col):
        Entity.__init__(self, row, col)

    def find_nearest_needed_entity(self, board: list, needed_entity: type, sight: int):
        """Finds the nearest needed entity within sight radius."""
        for check_sight in range(1,sight + 1):
            for check_row in range(self.row - check_sight, self.row + check_sight + 1):
                if 0 <= check_row < len(board):
                    for check_col in range(self.col - check_sight, self.col + check_sight + 1):
                        if 0 <= check_col < len(board[check_row]):
                            entity = board[check_row][check_col]

                            if isinstance(entity, needed_entity):
                                return entity

        return None

    def move_towards_entity(self, entity: Entity):
        if entity.row > self.row:
            self.row += 1
        elif entity.row < self.row:
            self.row -= 1
        if entity.col > self.col:
            self.col += 1
        elif entity.col < self.col:
            self.col -= 1

    def refuel_life_span(self):
        """Refuel the life span of the mobile entity"""
        self.age = 0

    def move_randomly(self, board: list):
        """Move to a random neighboring cell."""
        rows = len(board)
        cols = len(board[0])
        new_row = random.randrange(max(0, self.row - 1), min(rows, self.row + 2))
        new_col = random.randrange(max(0, self.col - 1), min(cols, self.col + 2))
        self.row = new_row
        self.col = new_col

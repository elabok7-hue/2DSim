class Entity:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.age = 0

    def increase_age(self):
        """Increase age"""
        self.age += 1

    def is_dead(self, death_age):
        """Check if entity is dead"""
        return self.age >= death_age

    def remove_from_board(self, board: list):
        """Remove an entity from the board."""
        board[self.row][self.col] = None

    def move_entity_on_board(self, old_row: int, old_col: int, board: list):
        """Update the board after an entity changed position."""

        if board[old_row][old_col] is self:
            board[old_row][old_col] = None

        if 0 <= self.row < len(board) and 0 <= self.col < len(board[0]):
            board[self.row][self.col] = self


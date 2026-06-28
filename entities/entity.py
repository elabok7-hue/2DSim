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
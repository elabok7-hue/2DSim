class Plant:
    t_plant = 10

    def __init__(self, row, col):
        self.age = 0
        self.row = row
        self.col = col

    def increase_age(self):
        """Increase age"""
        self.age += 1

    def is_dead(self):
        """Check if plant is dead"""
        return self.age >= self.t_plant

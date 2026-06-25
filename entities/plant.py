class Plant:
    t_plant = 10

    def __init__(self, row, col):
        self.age = 0
        self.row = row
        self.col = col

    def increase_age(self):
        self.age += 1

    def is_dead(self):
        return self.age >= self.t_plant

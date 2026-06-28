from entities.entity import Entity


class Plant(Entity):
    t_plant = 10

    def __init__(self, row, col):
        Entity.__init__(self, row, col)
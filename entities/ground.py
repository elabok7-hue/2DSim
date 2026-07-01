from entities.entity import Entity


class Ground(Entity):
    SIGN = "🟫"

    def __init__(self, row, col):
        Entity.__init__(self, row, col)

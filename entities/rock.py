from entities.entity import Entity


class Rock(Entity):
    SIGN = "🪨"

    def __init__(self, row, col):
        Entity.__init__(self, row, col)

    def print_entity(self):
        print(Rock.SIGN, end="")

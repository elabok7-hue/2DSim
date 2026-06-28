from entities.mobile_entity import MobileEntity


class Predator(MobileEntity):
    t_predator = 10
    r_predator_sight = 2
    t_cooldown = 10

    def __init__(self, row, col):
        MobileEntity.__init__(self, row, col)

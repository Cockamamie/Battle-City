from Assets.sprites import SpritesCreator
from random import randint, choice

sprites_creator = SpritesCreator()

width = height = 32
w = h = 416


def spawn_random(self, bonuses):
    pos = randint(0, 4) * w // 4, randint(0, 4) * h // 4
    power_up = choice(PowerUp.__subclasses__())
    bonuses.append(power_up(pos))


class PowerUp:
    def __init__(self, pos):
        self.position = pos


class Timer(PowerUp):
    def __init__(self, pos):
        self.image = sprites_creator.timer()
        super().__init__(pos)

    def freeze(self, enemies):
        pass


class Star(PowerUp):
    def __init__(self, pos):
        self.image = sprites_creator.star()
        super().__init__(pos)

    def upgrade(self):
        pass


class HP(PowerUp):
    def __init__(self, pos):
        self.image = sprites_creator.health()
        super().__init__(pos)

    def heal(self):
        pass

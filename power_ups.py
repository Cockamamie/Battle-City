from Assets.sprites import SpritesCreator
from random import randrange, choice
from pygame import Rect
from abc import ABCMeta, abstractmethod

sprites_creator = SpritesCreator()

width = height = 32


def spawn_random():
    pos = randrange(1, 11, 3) * width + width // 2,\
          randrange(1, 11, 3) * height + height // 2
    power_up = choice(PowerUp.__subclasses__())
    bonus = power_up(pos)
    return bonus


class PowerUp:
    __metaclass__ = ABCMeta

    def __init__(self, pos, image):
        self.position = pos
        self.image = image
        rect = image.get_rect()
        self.rect = Rect(self.position[0], self.position[1], rect.width, rect.height)
        self.is_visible = True

    def switch_visibility(self):
        self.is_visible = not self.is_visible

    @abstractmethod
    def perform(self, player, enemies, explosion_queue):
        pass


class Star(PowerUp):
    def __init__(self, pos):
        image = sprites_creator.star()
        super().__init__(pos, image)

    def perform(self, player, enemies, explosion_queue):
        player.upgrade()


class Grenade(PowerUp):
    def __init__(self, pos):
        image = sprites_creator.grenade()
        super().__init__(pos, image)

    def perform(self, player, enemies, explosion_queue):
        self.explode(enemies, explosion_queue)

    @staticmethod
    def explode(enemies, explosion_queue):
        copy = list(enemies)
        for enemy in copy:
            enemy.blow_up(explosion_queue)
            enemies.remove(enemy)



class HP(PowerUp):
    def __init__(self, pos):
        image = sprites_creator.health()
        super().__init__(pos, image)

    def perform(self, player, enemies, explosion_queue):
        player.increase_hp()

from Assets.sprites import SpritesCreator
from random import randrange, choice
from pygame import Rect
from abc import ABCMeta, abstractmethod
from sound import Sounds

sprites_creator = SpritesCreator()
sounds = Sounds()

width = height = 32


def spawn_random():
    pos = randrange(1, 11, 3) * width + width // 2,\
          randrange(1, 11, 3) * height + height // 2
    power_up = choice(PowerUp.__subclasses__())
    bonus = power_up(pos)
    sounds.bonus_appears.play()
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

    @staticmethod
    def on_pickup(player):
        player.score += 500

    @abstractmethod
    def perform(self, player, enemies, explosion_queue):
        pass

    def set_from_save(self, bonus):
        self.is_visible = bonus.is_visible


class Star(PowerUp):
    def __init__(self, pos):
        image = sprites_creator.star()
        super().__init__(pos, image)

    def perform(self, player, enemies, explosion_queue):
        sounds.star_bonus.play()
        player.upgrade()


class Grenade(PowerUp):
    def __init__(self, pos):
        image = sprites_creator.grenade()
        super().__init__(pos, image)

    def perform(self, player, enemies, explosion_queue):
        sounds.grenade_bonus.play()
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
        sounds.hp_bonus.play()
        player.increase_hp()

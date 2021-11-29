import pygame.sprite
from pygame import Rect
from typing import Tuple

from interfaces import MapObject
from Assets.sprites import SpritesCreator


class Brick(MapObject, pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().brick()
        self.rect = rect

    def kill(self) -> None:
        pygame.sprite.Sprite.kill(self)


class Steel(MapObject, pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().steel()
        self.rect = rect

    def kill(self) -> None:
        pygame.sprite.Sprite.kill(self)


class Grass(MapObject, pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().grass()
        self.rect = rect


class Water(MapObject, pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().water()[0]
        self.rect = rect


class Ice(MapObject, pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().ice()
        self.rect = rect


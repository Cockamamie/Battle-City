from pygame import Rect
from interfaces import MapObject
from Assets.sprites import SpritesCreator


class Brick(MapObject):
    def __init__(self, position: tuple[int, int]):
        self.image = SpritesCreator().brick()
        self.rect = self.image.get_rect()


class Steel(MapObject):
    def __init__(self, position: tuple[int, int]):
        self.image = SpritesCreator().steel()
        self.rect = self.image.get_rect()


class Grass(MapObject):
    def __init__(self, position: tuple[int, int]):
        self.image = SpritesCreator().grass()
        self.rect = self.image.get_rect()


class Water(MapObject):
    def __init__(self, position: tuple[int, int]):
        self.image = SpritesCreator().water()
        self.rect = self.image.get_rect()


class Ice(MapObject):
    def __init__(self, position: tuple[int, int]):
        self.image = SpritesCreator().ice()
        self.rect = self.image.get_rect()

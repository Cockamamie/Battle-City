import pygame.sprite
from Assets.sprites import SpritesCreator


class Brick(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().brick()
        self.rect = rect

    def kill(self) -> None:
        pygame.sprite.Sprite.kill(self)


class Steel(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().steel()
        self.rect = rect

    def kill(self) -> None:
        pygame.sprite.Sprite.kill(self)


class Grass(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().grass()
        self.rect = rect


class Water(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = SpritesCreator().water()
        self.image = self.images[0]
        self.rect = rect

    def switch_sprite(self):
        self.index = (self.index + 1) % 2
        self.image = self.images[self.index]


class Ice(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().ice()
        self.rect = rect

import pygame.sprite
from pygame import Rect
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


class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator() .eagle()
        self.rect = Rect((192, 384), (32, 32))

    def defeat(self):
        #закончить игру
        self.image = SpritesCreator().flag()

    def blow_up(self, explosion_queue):
        x = self.rect.x
        y = self.rect.y
        explosion_queue[0].append(((SpritesCreator().small_blast()), (x, y)))
        explosion_queue[1].append(((SpritesCreator().small_blast()), (x, y)))
        explosion_queue[2].append(((SpritesCreator().medium_blast()), (x, y)))
        explosion_queue[3].append(((SpritesCreator().medium_blast()), (x, y)))
        explosion_queue[4].append(((SpritesCreator().large_blast()), (x, y)))
        explosion_queue[5].append(((SpritesCreator().large_blast()), (x, y)))
        explosion_queue[6].append(((SpritesCreator().huge_blast()), (x - 16, y - 16)))
        explosion_queue[7].append(((SpritesCreator().huge_blast()), (x - 16, y - 16)))

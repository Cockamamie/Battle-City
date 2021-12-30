import pygame.sprite
from pygame import Rect
from Assets.sprites import SpritesCreator
from sound import Sounds

sounds = Sounds()


class Brick(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().brick()
        self.rect = rect
        self.sound = sounds.brick

    def kill(self) -> None:
        pygame.sprite.Sprite.kill(self)


class Steel(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = SpritesCreator().steel()
        self.rect = rect
        self.sound = sounds.steel

    def kill(self) -> None:
        pygame.sprite.Sprite.kill(self)
        self.sound.play()


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
        self.is_destroyed = False
        self.sound = sounds.destroy_eagle

    def defeat(self):
        self.is_destroyed = True
        self.image = SpritesCreator().flag()
        self.sound.play()

    def blow_up(self, explosion_queue):
        x, y = self.rect.center
        sc = SpritesCreator()
        blasts = [sc.small_blast, sc.medium_blast, sc.large_blast, sc.huge_blast]
        for i in range(4):
            explosion_queue[i].append((blasts[0](), (x - 16, y - 16)))
        for i in range(4, 8):
            explosion_queue[i].append((blasts[1](), (x - 16, y - 16)))
        for i in range(8, 12):
            explosion_queue[i].append((blasts[2](), (x - 16, y - 16)))
        for i in range(12, 16):
            explosion_queue[i].append((blasts[3](), (x - 32, y - 32)))

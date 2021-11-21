import pygame

from player import Player
from directions import Direction


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        player = Player((0, 0))
        run = True
        while run:
            window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            window.blit(player.image, player.position)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(Direction.Left)
            if keys[pygame.K_RIGHT]:
                player.move(Direction.Right)
            if keys[pygame.K_UP]:
                player.move(Direction.Up)
            if keys[pygame.K_DOWN]:
                player.move(Direction.Down)
            pygame.display.update()
        pygame.quit()
        quit()

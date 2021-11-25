import pygame

from player import Player
from enums import Direction
from level import Level
import landscape

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
empty_tiles = []


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        player = Player((0, 0))
        level_1 = Level(1).map
        for tile in level_1:
            if isinstance(tile, landscape.Empty):
                empty_tiles.append(tile.rect)
            elif isinstance(tile, landscape.Grass):
                upper.add(tile)
            elif isinstance(tile, (landscape.Ice, landscape.Water)):
                if isinstance(tile, landscape.Water):
                    obstacles.append(tile.rect)
                lower.add(tile)
            else:
                obstacles.append(tile.rect)
                medium.add(tile)
        current_direction = Direction.Down
        run = True
        while run:
            window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            lower.draw(window)
            window.blit(player.image, player.position)
            medium.draw(window)
            upper.draw(window)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and current_direction == Direction.Left:
                player.move(Direction.Left, obstacles)
            elif keys[pygame.K_RIGHT] and current_direction == Direction.Right:
                player.move(Direction.Right, obstacles)
            elif keys[pygame.K_UP] and current_direction == Direction.Up:
                player.move(Direction.Up, obstacles)
            elif keys[pygame.K_DOWN] and current_direction == Direction.Down:
                player.move(Direction.Down, obstacles)
            elif keys[pygame.K_LEFT]:
                player.move(Direction.Left, obstacles)
                current_direction = Direction.Left
            elif keys[pygame.K_RIGHT]:
                player.move(Direction.Right, obstacles)
                current_direction = Direction.Right
            elif keys[pygame.K_UP]:
                player.move(Direction.Up, obstacles)
                current_direction = Direction.Up
            elif keys[pygame.K_DOWN]:
                player.move(Direction.Down, obstacles)
                current_direction = Direction.Down
            pygame.display.update()
        pygame.quit()
        quit()

import pygame

from player import Player
from enums import Direction
from level import Level
import landscape

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
bullets = []
tanks = []
explosion_queue = [[] for i in range(4)]
clock = pygame.time.Clock()


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        level_1 = Level(1).map
        for tile in level_1:
            if isinstance(tile, landscape.Grass):
                upper.add(tile)
            elif isinstance(tile, landscape.Ice):
                lower.add(tile)
            else:
                obstacles.append(tile)
                medium.add(tile)
        current_direction = Direction.Down
        player = Player()
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
                player.move(Direction.Left, obstacles, tanks, bullets, explosion_queue)
            elif keys[pygame.K_RIGHT] and current_direction == Direction.Right:
                player.move(Direction.Right, obstacles, tanks, bullets, explosion_queue)
            elif keys[pygame.K_UP] and current_direction == Direction.Up:
                player.move(Direction.Up, obstacles, tanks, bullets, explosion_queue)
            elif keys[pygame.K_DOWN] and current_direction == Direction.Down:
                player.move(Direction.Down, obstacles, tanks, bullets, explosion_queue)
            elif keys[pygame.K_LEFT]:
                player.move(Direction.Left, obstacles, tanks, bullets, explosion_queue)
                current_direction = Direction.Left
            elif keys[pygame.K_RIGHT]:
                player.move(Direction.Right, obstacles, tanks, bullets, explosion_queue)
                current_direction = Direction.Right
            elif keys[pygame.K_UP]:
                player.move(Direction.Up, obstacles, tanks, bullets, explosion_queue)
                current_direction = Direction.Up
            elif keys[pygame.K_DOWN]:
                player.move(Direction.Down, obstacles, tanks, bullets, explosion_queue)
                current_direction = Direction.Down

            for bullet in bullets:
                window.blit(bullet.image, bullet.position)
                bullet.move(obstacles, tanks, bullets, explosion_queue)

            if keys[pygame.K_SPACE]:
                player.shoot(bullets)
            print(explosion_queue)
            for i in explosion_queue[0]:
                window.blit(i[0], i[1])
            del explosion_queue[0]
            explosion_queue.append([])
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

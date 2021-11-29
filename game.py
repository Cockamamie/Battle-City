import pygame

from player import Player
from enums import Direction
from level import Level, EnemyQueueCreator
import landscape

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
bullets = []
enemies = []
explosion_queue = [[] for i in range(4)]
clock = pygame.time.Clock()


class GameHelper:
    queue_creator = EnemyQueueCreator()

    def __init__(self, level_num):
        self.enemies_spawned = 0
        self.enemies_queue = self.queue_creator.generate_queue(level_num)

    def spawn_enemies(self):
        if len(enemies) >= 1:
            return
        self.enemies_spawned += 1
        is_bonus = False
        if self.enemies_spawned in [4, 11, 18]:
            is_bonus = True
        spawning_enemy = self.enemies_queue.pop(0)(is_bonus)
        enemies.append(spawning_enemy)


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @staticmethod
    def on_player_key_pressed(player, current_direction):
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
        if keys[pygame.K_SPACE]:
            player.shoot(bullets)

        return current_direction

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        game_helper = GameHelper(1)
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

            game_helper.spawn_enemies()

            for bullet in bullets:
                window.blit(bullet.image, bullet.position)
                bullet.move(obstacles, enemies, bullets, explosion_queue)

            for enemy in enemies:
                enemy.step(obstacles, bullets)
                window.blit(enemy.image, enemy.position)
            current_direction = self.on_player_key_pressed(player, current_direction)

            for i in explosion_queue[0]:
                window.blit(i[0], i[1])
            del explosion_queue[0]
            explosion_queue.append([])

            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

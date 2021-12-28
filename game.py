import pygame

from player import Player
from enums import Direction
from level import Level, EnemyQueueCreator
import landscape

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
empty_tiles = []
bullets = []
enemies = []
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

    def iter_events(self, water_switch, bonus_tank_switch):  # spawn power ups?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == water_switch:
                for obstacle in obstacles:
                    if isinstance(obstacle, landscape.Water):
                        obstacle.switch_sprite()
            elif event.type == bonus_tank_switch:
                for enemy in enemies:
                    if enemy.is_bonus:
                        enemy.switch_sprite()

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        game_helper = GameHelper(1)
        level_1 = Level(1).map
        water_switch = pygame.USEREVENT + 1
        bonus_tank_switch = pygame.USEREVENT + 2
        pygame.time.set_timer(water_switch, 750)
        pygame.time.set_timer(bonus_tank_switch, 250)
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
        player = Player()
        run = True
        while run:
            window.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.iter_events(water_switch, bonus_tank_switch)
            lower.draw(window)
            window.blit(player.image, player.position)
            medium.draw(window)
            upper.draw(window)
            game_helper.spawn_enemies()
            for bullet in bullets:
                window.blit(bullet.image, bullet.position)
                bullet.move()

            for enemy in enemies:
                enemy.step(obstacles, bullets)
                window.blit(enemy.image, enemy.position)
            current_direction = self.on_player_key_pressed(player, current_direction)

            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

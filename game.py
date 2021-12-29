import pygame

from player import Player
from enums import Direction
from game_helper import Level, GameHelper
import landscape

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
bullets = []
enemies = []
explosion_queue = [[] for i in range(4)]
clock = pygame.time.Clock()


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True

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

    def iter_events(self, game_helper, water_switch, bonus_tank_switch,
                    enemy_spawn):  # spawn power ups?
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
            elif event.type == enemy_spawn:
                game_helper.spawn_enemies(enemies)

    def run(self):
        lvl = 2
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        game_helper = GameHelper(lvl)
        water_switch = pygame.USEREVENT + 1
        bonus_tank_switch = pygame.USEREVENT + 2
        enemy_spawn = pygame.USEREVENT + 3
        pygame.time.set_timer(water_switch, 750)
        pygame.time.set_timer(bonus_tank_switch, 250)
        pygame.time.set_timer(enemy_spawn, 3000)
        level_1 = Level(lvl).map
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
        game_helper.spawn_enemies(enemies)
        while self.running:
            window.fill((0, 0, 0))
            self.iter_events(game_helper, water_switch, bonus_tank_switch,
                             enemy_spawn)
            lower.draw(window)
            window.blit(player.image, player.position)
            medium.draw(window)
            upper.draw(window)


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

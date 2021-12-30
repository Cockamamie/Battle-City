import pygame
from player import Player
from enums import Direction
from game_helper import Level, GameHelper
import landscape
from power_ups import spawn_random

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
bullets = []
enemies = []
bonus = None
explosion_queue = [[] for i in range(8)]
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
            player.move(Direction.Left, obstacles, enemies)
        elif keys[pygame.K_RIGHT] and current_direction == Direction.Right:
            player.move(Direction.Right, obstacles, enemies)
        elif keys[pygame.K_UP] and current_direction == Direction.Up:
            player.move(Direction.Up, obstacles, enemies)
        elif keys[pygame.K_DOWN] and current_direction == Direction.Down:
            player.move(Direction.Down, obstacles, enemies)
        elif keys[pygame.K_LEFT]:
            player.move(Direction.Left, obstacles, enemies)
            current_direction = Direction.Left
        elif keys[pygame.K_RIGHT]:
            player.move(Direction.Right, obstacles, enemies)
            current_direction = Direction.Right
        elif keys[pygame.K_UP]:
            player.move(Direction.Up, obstacles, enemies)
            current_direction = Direction.Up
        elif keys[pygame.K_DOWN]:
            player.move(Direction.Down, obstacles, enemies)
            current_direction = Direction.Down
        if keys[pygame.K_SPACE]:
            player.fire(bullets)

        return current_direction

    def iter_events(self, game_helper, water_switch, bonus_tank_switch,
                    enemy_spawn, bonus_blink):  # spawn power ups?
        global bonus
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
            elif event.type == bonus_blink:
                if bonus is not None:
                    bonus.switch_visibility()

    def run(self):
        global bonus
        lvl = 1
        pygame.init()
        window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Battle City")
        game_helper = GameHelper(lvl)
        water_switch = pygame.USEREVENT + 1
        bonus_tank_switch = pygame.USEREVENT + 2
        enemy_spawn = pygame.USEREVENT + 3
        bonus_blink = pygame.USEREVENT + 4
        pygame.time.set_timer(water_switch, 750)
        pygame.time.set_timer(bonus_tank_switch, 250)
        pygame.time.set_timer(enemy_spawn, 3000)
        pygame.time.set_timer(bonus_blink, 200)
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
                             enemy_spawn, bonus_blink)
            lower.draw(window)
            window.blit(player.image, player.position)

            for bullet in bullets:
                window.blit(bullet.image, bullet.position)
                spawn_bonus = bullet.move(obstacles, enemies, bullets, explosion_queue, player)
                if spawn_bonus:
                    bonus = spawn_random()
            for enemy in enemies:
                enemy.step(obstacles, bullets, enemies + [player])
                window.blit(enemy.image, enemy.position)
            current_direction = self.on_player_key_pressed(player, current_direction)

            medium.draw(window)
            upper.draw(window)

            for i in explosion_queue[0]:
                window.blit(i[0], i[1])
            del explosion_queue[0]
            explosion_queue.append([])

            if bonus is not None:
                if bonus.is_visible:
                    window.blit(bonus.image, bonus.position)
                pickup_res = player.try_pickup_bonus(bonus, enemies)
                if pickup_res:
                    bonus = None
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

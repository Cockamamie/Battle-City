import pygame
from player import Player
from enums import Direction
from game_helper import Level, GameHelper
import landscape
from power_ups import spawn_random
from timeit import default_timer as timer

pygame.init()

shoot_timer = timer()

lower = pygame.sprite.Group()
medium = pygame.sprite.Group()
upper = pygame.sprite.Group()

obstacles = []
bullets = []
enemies = []
bonus = None
explosion_queue = [[] for i in range(16)]
clock = pygame.time.Clock()

water_switch = pygame.USEREVENT + 1
bonus_tank_switch = pygame.USEREVENT + 2
enemy_spawn = pygame.USEREVENT + 3
bonus_blink = pygame.USEREVENT + 4
shoot_cool_down = pygame.USEREVENT + 5
pygame.time.set_timer(water_switch, 750)
pygame.time.set_timer(bonus_tank_switch, 250)
pygame.time.set_timer(enemy_spawn, 3000)
pygame.time.set_timer(bonus_blink, 200)
pygame.time.set_timer(shoot_cool_down, 200)

game_helper = None
player = None


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        self.running = True
        self.game_over = False
        self.lvl = 0

    @staticmethod
    def on_player_key_pressed(current_direction):
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

        global shoot_timer
        if keys[pygame.K_SPACE] and timer() - shoot_timer > 0.3:
            player.fire(bullets)
            shoot_timer = timer()

        return current_direction

    def iter_events(self):  # spawn power ups?
        global bonus
        global game_helper
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

    def iter_bullets(self):
        global bonus
        for bullet in bullets:
            self.window.blit(bullet.image, bullet.position)
            spawn_bonus = bullet.move(obstacles, enemies, bullets, explosion_queue, player)
            if spawn_bonus:
                bonus = spawn_random()

    def iter_enemies(self):
        for enemy in enemies:
            enemy.step(obstacles, bullets, enemies, player)
            self.window.blit(enemy.image, enemy.position)

    def process_explosion(self):
        for i in explosion_queue[0]:
            self.window.blit(i[0], i[1])
        explosion_queue.pop(0)
        explosion_queue.append([])

    def process_bonus(self):
        global bonus
        if bonus is not None:
            if bonus.is_visible:
                self.window.blit(bonus.image, bonus.position)
            pickup_res = player.try_pickup_bonus(bonus, enemies, explosion_queue)
            if pickup_res:
                bonus.on_pickup(player)
                bonus = None

    def generate_map(self):
        level = Level(self.lvl).map
        for tile in level:
            if isinstance(tile, landscape.Grass):
                upper.add(tile)
            elif isinstance(tile, landscape.Ice):
                lower.add(tile)
            else:
                obstacles.append(tile)
                medium.add(tile)

    def next_level(self):  # TODO set current direction outside this method
        global game_helper
        global obstacles
        global enemies
        lower.empty()
        medium.empty()
        upper.empty()
        obstacles = []
        enemies = []
        player.set_start_params()
        self.lvl = self.lvl + 1
        game_helper = GameHelper(self.lvl)
        self.generate_map()
        game_helper.spawn_enemies(enemies)

    def process_run(self, current_direction):
        lower.draw(self.window)
        self.window.blit(player.image, player.position)

        self.iter_events()
        self.iter_bullets()
        self.iter_enemies()

        medium.draw(self.window)
        upper.draw(self.window)

        self.process_explosion()
        self.process_bonus()
        return self.on_player_key_pressed(current_direction)

    def run(self):
        global bonus
        global player
        pygame.display.set_caption("Battle City")
        current_direction = Direction.Up
        player = Player()  # If game over
        self.next_level()
        game_helper.spawn_enemies(enemies)
        while self.running:
            self.window.fill((0, 0, 0))

            current_direction = self.process_run(current_direction)

            self.game_over = player.hp <= 0  # TODO: минус база

            if len(game_helper.enemies_queue) + len(enemies) == 0:
                self.next_level()
                current_direction = Direction.Up

            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

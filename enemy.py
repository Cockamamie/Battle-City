from random import randint, choice
from tank import Tank, Direction, Rect
from enums import MovingSpeed, ShootingSpeed
from timeit import default_timer as timer


class Enemy(Tank):
    def __init__(self, images, position,
                 bonus_images, health=100,
                 velocity=MovingSpeed.Default.value,
                 shouting_speed=ShootingSpeed.Default.value,
                 is_bonus=False):
        super().__init__(images, health, velocity, shouting_speed, position=position)
        self._is_bonus = is_bonus
        self._bonus_images = bonus_images
        self._bonus_index = 0
        self.timer = timer()

    @property
    def is_bonus(self):
        return self._is_bonus

    def set_random_direction(self):
        self._direction = choice(list(Direction))

    def first_period(self, is_intersecting):
        self.set_random_direction()
        self.check_tile_reach(is_intersecting)

    def change_behavior(self, is_intersecting):
        self.first_period(is_intersecting)

    def change_direction(self, is_intersecting):
        directions = [Direction.Up, Direction.Left,
                      Direction.Down, Direction.Right]
        if randint(1, 2) == 1:
            self.change_behavior(is_intersecting)
        elif randint(1, 2) == 1:
            self._direction = directions[(directions.index(self.direction) + 1) % 4]
        else:
            self._direction = directions[(directions.index(self.direction) - 1) % 4]

    def invert_direction(self):
        self._direction = Direction((-self.direction.value[0], -self.direction.value[1]))

    def try_shoot(self, bullets):
        if randint(1, 32) == 1:
            self.shoot(bullets)

    def check_tile_reach(self, is_intersecting):
        if self.position[0] % 32 == 0 and self.position[1] % 32 == 0 and randint(1, 16) == 1:
            self.change_behavior(is_intersecting)
        elif is_intersecting and randint(1, 4) == 1:
            if self.position[0] % 32 != 0 or self.position[1] % 32 != 0:
                self.invert_direction()
            else:
                self.change_direction(is_intersecting)

    def step(self, obstacles, bullets, enemies, player):
        tanks = enemies + [player]
        obstacles_rects = list(map(lambda x: x.rect, obstacles))
        tanks.remove(self)
        delta_pos = [delta * self.velocity for delta in self.direction.value]
        next_position = [x + y for x, y in zip(self.position, delta_pos)]
        intersecting_obstacles = Rect.collidelist(Rect(next_position, (32, 32)), obstacles_rects)
        self.check_tile_reach(intersecting_obstacles != -1)
        previous_pos = self.position
        self.move(self.direction, obstacles, tanks)
        if self.position == previous_pos and \
                timer() - self.timer > 0.5:
            self.change_direction(True)
        elif self.position != previous_pos:
            self.timer = timer()
        self.try_shoot(bullets)

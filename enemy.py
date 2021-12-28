from random import randint, choice
from tank import Tank, Direction, Rect


class Enemy(Tank):
    def __init__(self, images, bonus_images, health: int = 100,
                 velocity: int = 2, shouting_speed: int = 2,
                 is_bonus=False):
        super().__init__(images, health, velocity, shouting_speed)
        self._is_bonus = is_bonus
        self._bonus_images = bonus_images
        self._bonus_index = 0

    @property
    def is_bonus(self):
        return self._is_bonus

    def set_random_direction(self):
        self._direction = choice(list(Direction))

    def first_period(self, intersecting_index):
        self.set_random_direction()
        self.check_tile_reach(intersecting_index)

    def change_behavior(self, intersecting_index):
        self.first_period(intersecting_index)

    def change_direction(self, intersecting_index):
        directions = [Direction.Up, Direction.Left,
                      Direction.Down, Direction.Right]
        if randint(1, 2) == 1:
            self.change_behavior(intersecting_index)
        elif randint(1, 2) == 1:
            self._direction = directions[(directions.index(self.direction) + 1) % 4]
        else:
            self._direction = directions[(directions.index(self.direction) - 1) % 4]

    def invert_direction(self):
        self._direction = Direction((-self.direction.value[0], -self.direction.value[1]))

    def try_shoot(self, bullets):
        if randint(1, 32) == 1:
            self.shoot(bullets)

    def check_tile_reach(self, intersecting_index):
        if self.position[0] % 32 == 0 and self.position[1] % 32 == 0 and randint(1, 16) == 1:
            self.change_behavior(intersecting_index)
        elif intersecting_index != -1 and randint(1, 4) == 1:
            if self.position[0] % 32 != 0 or self.position[1] % 32 != 0:
                self.invert_direction()
            else:
                self.change_direction(intersecting_index)

    def step(self, obstacles, bullets):
        delta_pos = [delta * self.velocity for delta in self.direction.value]
        next_position = [x + y for x, y in zip(self.position, delta_pos)]
        intersecting_index = Rect.collidelist(Rect(next_position, (32, 32)), obstacles)
        self.check_tile_reach(intersecting_index)
        self.move(self.direction, obstacles)
        self.try_shoot(bullets)

from enums import Direction
from bullet import Bullet
from pygame import Rect, Surface

width = height = 32


class Tank:
    def __init__(self, images: dict[Direction, Surface], health=100, velocity=2,
                 shouting_speed=2, direction=Direction.Down, position=(0, 0), is_player=False):
        self._health = health
        self._velocity = velocity
        self._shouting_speed = shouting_speed
        self._direction = direction
        self._position = position
        self._is_player = is_player
        self._images = images
        self._image = images[direction]
        self._rect = self.image.get_rect()
        self.max_bullets_available = 1

    # region Properties
    @property
    def health(self):
        return self._health

    @property
    def velocity(self):
        return self._velocity

    @property
    def shouting_speed(self):
        return self._shouting_speed

    @property
    def direction(self):
        return self._direction

    @property
    def position(self):
        return self._position

    @property
    def is_player(self):
        return self._is_player

    @property
    def images(self):
        return self._images

    @property
    def image(self):
        return self._image

    @property
    def rect(self): return self._rect
    # endregion

    @staticmethod
    def in_map_bounds(position):
        return 0 <= position[0] < 385 and 0 <= position[1] < 385

    def __get_next_pos(self, direction, obstacles, enemies):
        delta_pos = [delta * self.velocity for delta in direction.value]
        next_position = [x + y for x, y in zip(self.position, delta_pos)]
        intersecting_index = Rect.collidelist(Rect(next_position, (32, 32)), obstacles)
        if intersecting_index == -1 and self.in_map_bounds(next_position):
            return next_position
        position = self.position
        if intersecting_index != -1:
            max_allowable_shift = 3 / 8 * width + 1
            intersecting_rect = obstacles[intersecting_index]
            left_intersection = intersecting_rect.x + intersecting_rect.width - position[0]
            above_intersection = intersecting_rect.y + intersecting_rect.height - position[1]
            right_intersection = position[0] + self.rect.width - intersecting_rect.x
            bot_intersection = position[1] + self.rect.height - intersecting_rect.y
            x, y = position
            if left_intersection < max_allowable_shift:
                x = intersecting_rect.x + intersecting_rect.width
            if right_intersection < max_allowable_shift:
                x = intersecting_rect.x - self.rect.width
            if above_intersection < max_allowable_shift:
                y = intersecting_rect.y + intersecting_rect.height
            if bot_intersection < max_allowable_shift:
                y = intersecting_rect.y - self.rect.height
            return [x, y]
        return position

    def move(self, direction: Direction, obstacles, enemies=None, bonuses=None):
        self._position = tuple(self.__get_next_pos(direction, obstacles, enemies))
        self._direction = direction
        self._image = self.images[direction]

    def take_damage(self, explosion_queue):
        self._health -= 100

    def shoot(self, bullets: list[Bullet]):
        bullet_width = bullet_height = 8
        bullet_pos_shift = {Direction.Up: ((width - bullet_width) // 2, 0),
                            Direction.Right: (width, (height - bullet_height) // 2),
                            Direction.Down: ((width - bullet_width) // 2, height),
                            Direction.Left: (0, (height - bullet_height) // 2)}
        bullet_pos = tuple([x + y for x, y in zip(self.position, bullet_pos_shift[self.direction])])
        bullets_shot = len(list(filter(lambda b: b.owner is self, bullets)))
        if bullets_shot >= self.max_bullets_available:
            return
        bullet = Bullet(self.direction, bullet_pos, self, self.is_player)
        bullets.append(bullet)

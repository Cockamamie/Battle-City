from typing import Tuple, Dict, List

from enums import Direction
from bullet import Bullet
from pygame import Rect
from landscape import Brick, Steel, Water

width = height = 32


class Tank:
    def __init__(self, health: int = 100, velocity: int = 2, shouting_speed: int = 2,
                 direction: Direction = Direction.Down, position: Tuple[int, int] = (0, 0),
                 is_player: bool = False, images: Dict[Direction, any] = None):
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
    def rect(self):
        return self._rect

    def take_damage(self, explosion_queue):
        self._health -= 100

    def move(self, direction: Direction, obstacles, enemies, bullets, explosion_queue, bonuses=None):
        allowable_shift = 3 / 8 * width + 1
        previous_pos = self.position
        delta_pos = [delta * self.velocity for delta in direction.value]
        self._position = [x + y for x, y in zip(self.position, delta_pos)]
        current_rect = Rect(self.position, (width, height))
        intersecting_obs_list = [(i.rect.colliderect(current_rect) and
                                  isinstance(i, (Brick, Steel, Water))) for i in obstacles]
        intersection_index = 0
        intersections_count = -1
        for i in range(len(intersecting_obs_list)):
            if intersecting_obs_list[i]:
                intersection_index = i
                intersections_count += 1
        if intersections_count == 0:
            intersecting_rect = obstacles[intersection_index].rect
            self._position = previous_pos
            if intersecting_rect.x + intersecting_rect.width - self.position[0] < allowable_shift \
                    and intersecting_rect.y + intersecting_rect.height - self.position[1] < allowable_shift:
                self._position = [intersecting_rect.x + intersecting_rect.width,
                                  intersecting_rect.y + intersecting_rect.height]
            elif self.position[0] + self.rect.width - intersecting_rect.x < allowable_shift \
                    and intersecting_rect.y + intersecting_rect.height - self.position[1] < allowable_shift:
                self._position = [intersecting_rect.x - self.rect.width,
                                  intersecting_rect.y + intersecting_rect.height]
            elif intersecting_rect.x + intersecting_rect.width - self.position[0] < allowable_shift \
                    and self.position[1] + self.rect.height - intersecting_rect.y < allowable_shift:
                self._position = [intersecting_rect.x + intersecting_rect.width,
                                  intersecting_rect.y - self.rect.height]
            elif self.position[0] + self.rect.width - intersecting_rect.x < allowable_shift \
                    and self.position[1] + self.rect.height - intersecting_rect.y < allowable_shift:
                self._position = [intersecting_rect.x - self.rect.width,
                                  intersecting_rect.y - self.rect.height]
            else:
                self._position = previous_pos
        elif intersections_count > 0:
            self._position = previous_pos
        if not (0 <= self.position[0] < 385 and 0 <= self.position[1] < 385):
            self._position = previous_pos
        self._direction = direction
        self._image = self.images[direction]

    def shoot(self, bullets: List[Bullet]):
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


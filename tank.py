from enums import Direction
from bullet import Bullet
from pygame import Rect


class Tank:
    def __init__(self, health: int = 100, velocity: int = 2, shouting_speed: int = 2,
                 direction: Direction = Direction.Down, position: tuple[int, int] = (0, 0),
                 is_player: bool = False, images: dict[Direction, any] = None):
        self._health = health
        self._velocity = velocity
        self._shouting_speed = shouting_speed
        self._direction = direction
        self._position = position
        self._is_player = is_player
        self._images = images
        self._image = images[direction]
        self.max_bullets_available = 1

    @property
    def health(self): return self._health

    @property
    def velocity(self): return self._velocity

    @property
    def shouting_speed(self): return self._shouting_speed

    @property
    def direction(self): return self._direction

    @property
    def position(self): return self._position

    @property
    def is_player(self): return self._is_player

    @property
    def images(self): return self._images

    @property
    def image(self): return self._image

    def move(self, direction: Direction, obstacles, enemies=None, bonuses=None):
        previous_pos = self.position
        delta_pos = [delta * self.velocity for delta in direction.value]
        self._position = tuple([x + y for x, y in zip(self.position, delta_pos)])
        rect = Rect(self.position, (32, 32))
        is_moving_possible = rect.collidelist(obstacles) != -1 and not\
            (0 <= self.position[0] < 385 and 0 <= self.position[1] < 385)
        if not is_moving_possible:
            self._position = previous_pos
        # for bonus in bonuses:
        #     if rect.colliderect(bonus.rect):
        #         self.bonus = bonus
        self._direction = direction
        self._image = self.images[direction]

    def shoot(self, bullets: list[Bullet]):
        bullet_width = bullet_height = 8
        width = self.image.get_width()
        height = self.image.get_height()
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

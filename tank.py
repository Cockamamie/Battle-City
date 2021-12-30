from enums import Direction, MovingSpeed, ShootingSpeed
from bullet import Bullet
from pygame import Rect, Surface
from Assets.sprites import SpritesCreator
from sound import Sounds

width = height = 32

sounds = Sounds()


class Tank:
    def __init__(self, images, health=100,
                 velocity=MovingSpeed.Default.value,
                 shouting_speed=ShootingSpeed.Default.value,
                 direction=Direction.Down, position=(0, 0), is_player=False):
        self._health = health
        self._velocity = velocity
        self.shouting_speed = shouting_speed
        self._direction = direction
        self._position = position
        self._is_player = is_player
        self.images = images
        self._image = images[direction]
        self._rect = self.image.get_rect()
        self.max_bullets_available = 1
        self._stars = 0
        self.destroy_enemy_sound = sounds.destroy_enemy

    # region Properties
    @property
    def health(self):
        return self._health

    @property
    def velocity(self):
        return self._velocity

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
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    # endregion

    @staticmethod
    def in_map_bounds(position):
        return 0 <= position[0] < 385 and 0 <= position[1] < 385

    def __get_next_pos(self, direction, obstacles, tanks):
        enemies = tanks
        tank_size = (width, height)
        delta_pos = [delta * self.velocity for delta in direction.value]
        next_position = [x + y for x, y in zip(self.position, delta_pos)]

        intersecting_index = Rect.collidelist(Rect(next_position, tank_size), obstacles)

        intersecting_enemies_index = \
            Rect.collidelist(Rect(next_position, tank_size),
                             list(map(lambda x: (x.position, tank_size), enemies)))

        if intersecting_index + intersecting_enemies_index == -2 and self.in_map_bounds(next_position):
            return next_position
        position = self.position
        if intersecting_index != -1:
            max_allowable_shift = 3 / 8 * width + 1
            intersecting_rect = obstacles[intersecting_index].rect
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

            if Rect.collidelist(Rect((x, y), tank_size),
                                list(map(lambda x: (x.position, tank_size), enemies))) != -1:
                x, y = position
            return [x, y]
        return position

    def move(self, direction: Direction, obstacles, enemies):
        self._position = tuple(self.__get_next_pos(direction, obstacles, enemies))
        self._direction = direction
        self._image = self.images[direction]

    def take_damage(self, explosion_queue, enemies, index):
        self._health -= 100
        if self._health <= 0:
            self.blow_up(explosion_queue)
            self.destroy(enemies, index)

    def blow_up(self, explosion_queue):
        self.destroy_enemy_sound.play()
        x, y = self.position[0], self.position[1]
        sc = SpritesCreator()
        blasts = [sc.small_blast, sc.medium_blast, sc.large_blast]
        for i in range(3):
            explosion_queue[i].append((blasts[i](), (x, y)))

    @staticmethod
    def destroy(enemies, index):
        if index < len(enemies):
            enemies.pop(index)

    def shoot(self, bullets, is_steel_destroyable=False):
        bullet_width = bullet_height = 8
        bullet_pos_shift = {Direction.Up: ((width - bullet_width) // 2, 0),
                            Direction.Right: (width, (height - bullet_height) // 2),
                            Direction.Down: ((width - bullet_width) // 2, height),
                            Direction.Left: (0, (height - bullet_height) // 2)}
        bullet_pos = tuple([x + y for x, y in zip(self.position, bullet_pos_shift[self.direction])])
        bullets_shot = len(list(filter(lambda b: b.owner is self, bullets)))
        if bullets_shot >= self.max_bullets_available:
            return
        bullet = Bullet(self.direction, bullet_pos, self, self.is_player,
                        self.shouting_speed, is_steel_destroyable)
        bullets.append(bullet)

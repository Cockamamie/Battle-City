import pygame
from pygame import Rect

import tank
from enums import Direction
from Assets.sprites import SpritesCreator
from landscape import Brick, Steel


class Bullet:
    def __init__(self, direction: Direction, start_position: (int, int),
                 owner, belongs_player=False,
                 velocity=5, is_steel_destroyable=False):
        self.__direction = direction
        self.__position = start_position
        self.velocity = velocity
        self.__owner = owner
        self.__belongs_player = belongs_player
        self.__is_steel_destroyable = is_steel_destroyable

        sprites_creator = SpritesCreator()
        self.image = sprites_creator.bullet()[direction]
        self.rect = self.image.get_rect()
        self.blasts = [sprites_creator.small_blast(),
                       sprites_creator.medium_blast()]

    @property
    def direction(self):
        return self.__direction

    @property
    def position(self):
        return self.__position

    @property
    def owner(self):
        return self.__owner

    # @property
    # def velocity(self): return self.velocity

    @property
    def belongs_player(self):
        return self.__belongs_player

    @property
    def is_steel_destroyable(self):
        return self.__is_steel_destroyable

    def blow_up(self, explosion_queue):
        x = self.position[0] - 12 if self.position[0] - 12 >= 0 else 0
        y = self.position[1] - 12 if self.position[1] - 12 >= 0 else 0
        explosion_queue[0].append(((SpritesCreator().small_blast()), (x, y)))
        explosion_queue[1].append(((SpritesCreator().medium_blast()), (x, y)))
        explosion_queue[2].append(((SpritesCreator().large_blast()), (x, y)))

    def move(self, obstacles, tanks, bullets, explosion_queue):
        blow_up_bullet = True
        delta_pos = [delta * self.velocity for delta in self.direction.value]
        self.__position = tuple([x + y for x, y in zip(self.position, delta_pos)])
        current_rect = Rect(self.position, (8, 8))
        intersecting_obs_list = [(i.rect.colliderect(current_rect) and
                                  isinstance(i, (Brick,  Steel))) for i in obstacles]
        intersecting_obs_index = -1
        shift = 0
        for i in range(len(intersecting_obs_list)):
            if intersecting_obs_list[i]:
                intersecting_obs_index = 0
                if isinstance(obstacles[i - shift], Steel) and not self.__is_steel_destroyable:
                    continue
                obstacles[i - shift].kill()
                del obstacles[i - shift]
                shift += 1

        intersecting_tanks_index = Rect.collidelist(Rect(self.position, (8, 8)),
                                                    list(map(lambda x: x.rect, tanks)))
        intersecting_bull_index = Rect.collidelist(Rect(self.position, (8, 8)),
                                                   list(map(lambda x: x.rect, bullets)))
        if intersecting_bull_index != -1:
            intersecting_bullet = bullets[intersecting_bull_index]
            if not(intersecting_bullet.belongs_player or self.belongs_player):
                blow_up_bullet = False
        if intersecting_obs_index + intersecting_bull_index + intersecting_tanks_index != -3 or \
                not (0 <= self.position[0] < 409 and 0 <= self.position[1] < 409):
            for i in range(len(bullets)):
                if self.rect == bullets[i].rect:
                    del bullets[i]
                    break
            if blow_up_bullet:
                self.blow_up(explosion_queue)
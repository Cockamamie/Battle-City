import pygame
from pygame import Rect

import tank
from enums import Direction
from Assets.sprites import SpritesCreator
from landscape import Brick, Steel, Eagle


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

    def move(self, obstacles, enemies, bullets, explosion_queue, player):
        spawn_bonus = False
        tanks = enemies + [player]
        blow_up_bullet = True
        erase_bullet = True
        delta_pos = [delta * self.velocity for delta in self.direction.value]
        self.__position = tuple([x + y for x, y in zip(self.position, delta_pos)])
        current_rect = Rect(self.position, (8, 8))
        intersecting_obs_list = [(i.rect.colliderect(current_rect) and
                                  isinstance(i, (Brick,  Steel, Eagle))) for i in obstacles]
        intersecting_obs_index = -1
        shift = 0
        for i in range(len(intersecting_obs_list)):
            if intersecting_obs_list[i]:
                intersecting_obs_index = 0
                if isinstance(obstacles[i - shift], Eagle):
                    obstacles[i - shift].blow_up(explosion_queue)
                    obstacles[i - shift].defeat()
                    continue
                if isinstance(obstacles[i - shift], Steel) and not self.__is_steel_destroyable:
                    continue
                obstacles[i - shift].kill()
                del obstacles[i - shift]
                shift += 1

        not_own1 = []
        for e in tanks:
            not_own1.append(e)
        for t in not_own1:
            if self.owner.position == t.position:
                not_own1.remove(t)
                break
        intersecting_tanks_index = Rect.collidelist(Rect(self.position, (8, 8)),
                                                    list(map(lambda x: (x.position, (32, 32)), not_own1)))
        not_own = []
        for e in bullets:
            not_own.append(e)
        for b in not_own:
            if self.position == b.position:
                not_own.remove(b)
                break
        intersecting_bull_index = Rect.collidelist(Rect(self.position, (8, 8)),
                                                   list(map(lambda x: (x.position, (8, 8)), not_own)))

        if intersecting_bull_index != -1:
            for i in range(len(bullets)):
                if not_own[intersecting_bull_index].position == bullets[i].position:
                    intersecting_bull_index = i
                    break
            intersecting_bullet = bullets[intersecting_bull_index]
            if not(intersecting_bullet.belongs_player or self.belongs_player):
                blow_up_bullet = False
            else:
                del bullets[intersecting_bull_index]
                for i in range(len(bullets)):
                    if bullets[i].position == self.position:
                        del bullets[i]
                        break
        if intersecting_obs_index + intersecting_tanks_index != -2 or \
                not (0 <= self.position[0] < 409 and 0 <= self.position[1] < 409):
            if intersecting_tanks_index != -1:
                for i in range(len(tanks)):
                    if tanks[i].position == not_own1[intersecting_tanks_index].position:
                        intersecting_tanks_index = i
                        break
                intersecting_tank = tanks[intersecting_tanks_index]
                if self.belongs_player and intersecting_tank.is_bonus:
                    spawn_bonus = True
                    intersecting_tank.is_bonus = False
                else:
                    spawn_bonus = False
                if intersecting_tank.is_player or self.belongs_player:
                    for e in tanks:
                        if e.position == intersecting_tank.position:
                            intersecting_tank.take_damage(explosion_queue, enemies,
                                                          intersecting_tanks_index, player)
                else:
                    blow_up_bullet = False
                    erase_bullet = False
            if erase_bullet:
                for i in range(len(bullets)):
                    if self.position == bullets[i].position:
                        del bullets[i]
                        break
            if blow_up_bullet:
                self.blow_up(explosion_queue)
        return spawn_bonus

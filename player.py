from typing import Tuple

import pygame

from Assets.sprites import SpritesCreator
from enums import Direction


class Player:
    def __init__(self, start: Tuple[int, int]):
        self.velocity = 0.15
        self.position = start

        sprites_creator = SpritesCreator()
        self.no_stars = sprites_creator.no_stars_player()
        # self.one_star = sprites_creator.one_star_player()
        # self.two_stars = sprites_creator.two_stars_player()
        # self.three_stars = sprites_creator.three_stars_player()
        self.image = self.no_stars[Direction.Up]
        self.rect = self.image.get_rect()

    def move(self, direction: Direction, obstacles) -> None:
        previous_pos = self.position
        delta_pos = [delta * self.velocity for delta in direction.value]
        self.position = [x + y for x, y in zip(self.position, delta_pos)]
        intersecting_index = pygame.Rect.collidelist(pygame.Rect(self.position, (32, 32)), obstacles)
        if intersecting_index != -1:
            intersecting_rect = obstacles[intersecting_index]
            self.position = previous_pos
            if intersecting_rect.x + intersecting_rect.width - self.position[0] < 13 \
                    and intersecting_rect.y + intersecting_rect.height - self.position[1] < 13:
                self.position = [intersecting_rect.x + intersecting_rect.width,
                                 intersecting_rect.y + intersecting_rect.height]
            elif self.position[0] + self.rect.width - intersecting_rect.x < 13 \
                    and intersecting_rect.y + intersecting_rect.height - self.position[1] < 13:
                self.position = [intersecting_rect.x - self.rect.width,
                                 intersecting_rect.y + intersecting_rect.height]
            elif intersecting_rect.x + intersecting_rect.width - self.position[0] < 13 \
                    and self.position[1] + self.rect.height - intersecting_rect.y < 13:
                self.position = [intersecting_rect.x + intersecting_rect.width,
                                 intersecting_rect.y - self.rect.height]
            elif self.position[0] + self.rect.width - intersecting_rect.x < 13 \
                    and self.position[1] + self.rect.height - intersecting_rect.y < 13:
                self.position = [intersecting_rect.x - self.rect.width,
                                 intersecting_rect.y - self.rect.height]
            else:
                self.position = previous_pos
        if not (0 <= self.position[0] < 385 and 0 <= self.position[1] < 385):
            self.position = previous_pos
        self.image = self.no_stars[direction]
    
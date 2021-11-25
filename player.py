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

    def move(self, direction: Direction, obstacles) -> None:
        previous_pos = self.position
        delta_pos = [delta * self.velocity for delta in direction.value]
        self.position = [x + y for x, y in zip(self.position, delta_pos)]
        intersecting_index = pygame.Rect.collidelist(pygame.Rect(self.position, (32, 32)), obstacles)
        if intersecting_index != -1 or not (0 <= self.position[0] < 385 and 0 <= self.position[1] < 385):
            self.position = previous_pos
        self.image = self.no_stars[direction]
    
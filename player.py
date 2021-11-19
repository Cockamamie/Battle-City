from Sprites.sprites import SpritesCreator
from directions import Direction


class Player:
    def __init__(self, start: tuple[int, int]):
        self.velocity = 2
        self.position = start

        sprites_creator = SpritesCreator()
        self.no_stars = sprites_creator.no_stars_player()
        # self.one_star = sprites_creator.one_star_player()
        # self.two_stars = sprites_creator.two_stars_player()
        # self.three_stars = sprites_creator.three_stars_player()
        self.image = self.no_stars[Direction.Up]

    def move(self, direction: Direction) -> None:
        delta_pos = [delta * self.velocity for delta in direction.value]
        self.position = tuple([x + y for x, y in zip(self.position, delta_pos)])
        self.image = self.no_stars[direction]
